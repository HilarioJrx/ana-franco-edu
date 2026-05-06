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
