from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum, Count, Avg
from .models import Funcionario, Order


def home(request):
    """View da página inicial"""
    context = {
        'total_funcionarios': Funcionario.objects.count(),
        'total_pedidos': Order.objects.count(),
        'pedidos_pendentes': Order.objects.filter(status='pending').count(),
        'valor_total_pedidos': Order.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0,
    }
    return render(request, 'home.html', context)


class PainelView(LoginRequiredMixin, TemplateView):
    """Painel administrativo"""
    template_name = 'painel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_funcionarios'] = Funcionario.objects.count()
        context['total_pedidos'] = Order.objects.count()
        context['pedidos_pendentes'] = Order.objects.filter(status='pending').count()
        context['pedidos_concluidos'] = Order.objects.filter(status='completed').count()
        context['valor_total_pedidos'] = Order.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        context['valor_medio_pedidos'] = Order.objects.aggregate(Avg('valor_total'))['valor_total__avg'] or 0
        return context


@login_required
def perfil(request):
    """Perfil do usuário logado"""
    return render(request, 'perfil.html')


class FuncionarioListView(LoginRequiredMixin, ListView):
    """Listagem de funcionários"""
    model = Funcionario
    template_name = 'funcionarios/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Funcionario.objects.all()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) | Q(email__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class FuncionarioDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de um funcionário"""
    model = Funcionario
    template_name = 'funcionarios/funcionario_detail.html'
    context_object_name = 'funcionario'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pedidos'] = self.object.orders.all()
        context['total_pedidos'] = self.object.orders.count()
        context['valor_total_pedidos'] = self.object.orders.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        return context


class OrderListView(LoginRequiredMixin, ListView):
    """Listagem de pedidos"""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'pedidos'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Order.objects.select_related('funcionario').all()
        
        # Filtro por status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filtro por prioridade
        prioridade = self.request.GET.get('prioridade')
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade)
        
        # Busca por número de pedido ou descrição
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(numero_pedido__icontains=search) | Q(descricao__icontains=search)
            )
        
        return queryset.order_by('-data_pedido')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        context['prioridade_choices'] = Order.PRIORITY_CHOICES
        context['search_query'] = self.request.GET.get('q', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['prioridade_filter'] = self.request.GET.get('prioridade', '')
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de um pedido"""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'pedido'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order.STATUS_CHOICES
        context['prioridade_choices'] = Order.PRIORITY_CHOICES
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard com estatísticas"""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas gerais
        context['total_funcionarios'] = Funcionario.objects.count()
        context['total_pedidos'] = Order.objects.count()
        
        # Estatísticas de pedidos por status
        context['pedidos_por_status'] = {
            'pending': Order.objects.filter(status='pending').count(),
            'processing': Order.objects.filter(status='processing').count(),
            'completed': Order.objects.filter(status='completed').count(),
            'cancelled': Order.objects.filter(status='cancelled').count(),
        }
        
        # Estatísticas de pedidos por prioridade
        context['pedidos_por_prioridade'] = {
            'low': Order.objects.filter(prioridade='low').count(),
            'medium': Order.objects.filter(prioridade='medium').count(),
            'high': Order.objects.filter(prioridade='high').count(),
            'urgent': Order.objects.filter(prioridade='urgent').count(),
        }
        
        # Valores de pedidos
        context['valor_total_pedidos'] = Order.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        context['valor_medio_pedidos'] = Order.objects.aggregate(Avg('valor_total'))['valor_total__avg'] or 0
        
        # Últimos pedidos
        context['ultimos_pedidos'] = Order.objects.select_related('funcionario').order_by('-created_at')[:5]
        
        # Funcionários com mais pedidos
        context['funcionarios_top'] = Funcionario.objects.annotate(
            total_pedidos=Count('orders')
        ).order_by('-total_pedidos')[:5]
        
        return context
