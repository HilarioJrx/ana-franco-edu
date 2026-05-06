from django.contrib import admin
from .models import Category, Feed

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('categories', 'author', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('categories',)
