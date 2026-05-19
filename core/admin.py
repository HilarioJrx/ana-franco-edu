from django.contrib import admin
from .models import Category, Feed, UniformItem, UniformOrder, UniformOrderItem

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

    class Media:
        css = {
            'all': (
                'https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css',
            )
        }
        js = (
            'https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js',
            'js/admin_quill.js',
        )


@admin.register(UniformItem)
class UniformItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'color', 'price', 'available')
    list_filter = ('item_type', 'available', 'color')
    search_fields = ('name', 'color', 'description')
    list_editable = ('price', 'available')


class UniformOrderItemInline(admin.TabularInline):
    model = UniformOrderItem
    extra = 0
    readonly_fields = ('subtotal_display',)

    def subtotal_display(self, obj):
        if obj.pk:
            return f"R$ {obj.subtotal:.2f}"
        return "-"
    subtotal_display.short_description = "Subtotal"


@admin.register(UniformOrder)
class UniformOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_display', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('user', 'created_at', 'total_display')
    inlines = [UniformOrderItemInline]

    def total_display(self, obj):
        return f"R$ {obj.total:.2f}"
    total_display.short_description = "Total"
