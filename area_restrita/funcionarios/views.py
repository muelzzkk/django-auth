from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'home.html')


class PainelView(LoginRequiredMixin, TemplateView):
    template_name = 'painel.html'


@login_required
def perfil(request):
    return render(request, 'perfil.html')