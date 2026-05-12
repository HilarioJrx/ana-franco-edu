from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#000000', help_text="Código Hex da cor (ex: #FF0000)")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Feed(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_key = models.CharField(max_length=255, blank=True, null=True, help_text="Nome/caminho da imagem no bucket")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='feeds')

    def __str__(self):
        return self.title


UNIFORM_TYPE_CHOICES = [
    ('camiseta', 'Camiseta'),
    ('moletom', 'Moletom'),
    ('outro', 'Outro'),
]


class UniformItem(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome da peça")
    item_type = models.CharField(
        max_length=20, choices=UNIFORM_TYPE_CHOICES, default='camiseta',
        verbose_name="Tipo"
    )
    color = models.CharField(max_length=100, verbose_name="Cor")
    description = models.TextField(blank=True, verbose_name="Descrição")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço (R$)")
    available = models.BooleanField(default=True, verbose_name="Disponível")
    image_key = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Nome/caminho da imagem no bucket",
        verbose_name="Imagem"
    )

    class Meta:
        verbose_name = "Item de Uniforme"
        verbose_name_plural = "Itens de Uniforme"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} — {self.color}"


UNIFORM_ORDER_STATUS = [
    ('pendente', 'Pendente'),
    ('preparando', 'Em Preparação'),
    ('disponivel', 'Disponível para Retirada'),
    ('entregue', 'Entregue'),
    ('cancelado', 'Cancelado'),
]

class UniformOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='uniform_orders',
        verbose_name="Aluno"
    )
    status = models.CharField(
        max_length=20, choices=UNIFORM_ORDER_STATUS, default='pendente',
        verbose_name="Status"
    )
    notes = models.TextField(blank=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do pedido")

    class Meta:
        verbose_name = "Pedido de Uniforme"
        verbose_name_plural = "Pedidos de Uniforme"
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.pk} — {self.user.get_full_name() or self.user.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


SIZE_CHOICES = [
    ('PP', 'PP'),
    ('P', 'P'),
    ('M', 'M'),
    ('G', 'G'),
    ('GG', 'GG'),
    ('XG', 'XG'),
]


class UniformOrderItem(models.Model):
    order = models.ForeignKey(
        UniformOrder, on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Pedido"
    )
    uniform_item = models.ForeignKey(
        UniformItem, on_delete=models.PROTECT,
        verbose_name="Item"
    )
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, verbose_name="Tamanho")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.uniform_item.name} ({self.size}) x{self.quantity}"

    @property
    def subtotal(self):
        return self.uniform_item.price * self.quantity
