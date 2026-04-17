from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Manager que retorna apenas registros não deletados por padrão"""
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """Modelo base com campos de auditoria e soft delete"""
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Criação',
        help_text='Data e hora de criação do registro',
        editable=False
    )
    updated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Atualização',
        help_text='Data e hora da última atualização'
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Deletado?',
        help_text='Marcado como deletado (soft delete)'
    )
    
    # Manager padrão (apenas registros ativos)
    objects = SoftDeleteManager()
    
    # Manager para todos os registros (inclusive deletados)
    all_objects = models.Manager()
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def soft_delete(self):
        """Realiza um soft delete do registro"""
        self.is_deleted = True
        self.updated_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restaura um registro deletado"""
        self.is_deleted = False
        self.updated_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f"{self.__class__.__name__} - {self.id}"


class Funcionario(BaseModel):
    """Modelo de Funcionário com auditoria e soft delete"""
    
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome completo',
        help_text='Nome completo do funcionário'
    )
    cargo = models.CharField(
        max_length=50,
        verbose_name='Cargo',
        help_text='Cargo do funcionário'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Email único do funcionário'
    )
    salario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Salário',
        help_text='Salário do funcionário'
    )
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.cargo}"


class Order(BaseModel):
    """Modelo de Pedidos com auditoria e soft delete"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    numero_pedido = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número do Pedido',
        help_text='Identificador único do pedido'
    )
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Funcionário Responsável',
        related_name='orders'
    )
    data_pedido = models.DateField(
        auto_now_add=True,
        verbose_name='Data do Pedido'
    )
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor Total'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status',
        help_text='Status atual do pedido'
    )
    prioridade = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='Prioridade'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição detalhada do pedido'
    )
    data_entrega = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Entrega'
    )
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data_pedido']
        indexes = [
            models.Index(fields=['numero_pedido']),
            models.Index(fields=['status']),
            models.Index(fields=['-data_pedido']),
        ]
    
    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.get_status_display()}"
    
    def marcar_como_processando(self):
        """Marca o pedido como processando"""
        self.status = 'processing'
        self.save()
    
    def marcar_como_concluido(self):
        """Marca o pedido como concluído"""
        self.status = 'completed'
        self.save()
    
    def cancelar(self):
        """Cancela o pedido"""
        self.status = 'cancelled'
        self.save()

