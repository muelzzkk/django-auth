from django.contrib import admin
from .models import Funcionario, Order


class BaseModelAdmin(admin.ModelAdmin):
    """Admin base com campos de auditoria"""
    readonly_fields = ('created_at', 'updated_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ()  # Será preenchido pelas subclasses
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',),
            'description': 'Informações de auditoria do registro'
        }),
    )


@admin.register(Funcionario)
class FuncionarioAdmin(BaseModelAdmin):
    """Admin customizado para Funcionário"""
    list_display = ('nome', 'cargo', 'email', 'salario', 'created_at', 'is_deleted')
    list_filter = ('cargo', 'created_at', 'is_deleted')
    search_fields = ('nome', 'email', 'cargo')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações do Funcionário', {
            'fields': ('nome', 'cargo', 'email', 'salario')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    """Admin customizado para Pedido"""
    list_display = ('numero_pedido', 'funcionario', 'status', 'prioridade', 'valor_total', 'data_pedido', 'is_deleted')
    list_filter = ('status', 'prioridade', 'data_pedido', 'is_deleted')
    search_fields = ('numero_pedido', 'descricao', 'funcionario__nome')
    ordering = ('-data_pedido',)
    readonly_fields = ('created_at', 'updated_at', 'is_deleted', 'data_pedido')
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('numero_pedido', 'funcionario', 'valor_total')
        }),
        ('Status e Prioridade', {
            'fields': ('status', 'prioridade')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'data_entrega'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('data_pedido',),
            'classes': ('collapse',),
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',),
        }),
    )
