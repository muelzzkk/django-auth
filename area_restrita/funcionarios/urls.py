from django.urls import path
from . import views

app_name = 'funcionarios'

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),
    
    # Painel
    path('painel/', views.PainelView.as_view(), name='painel'),
    
    # Perfil
    path('perfil/', views.perfil, name='perfil'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Funcionários
    path('funcionarios/', views.FuncionarioListView.as_view(), name='funcionario_list'),
    path('funcionarios/<int:pk>/', views.FuncionarioDetailView.as_view(), name='funcionario_detail'),
    
    # Pedidos
    path('pedidos/', views.OrderListView.as_view(), name='order_list'),
    path('pedidos/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
