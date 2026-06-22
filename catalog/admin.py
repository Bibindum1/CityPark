from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Dish

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'dishes_count', 'view_dishes_link']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['id']
    fieldsets = [
        ('Основная информация', {
            'fields': ['name'],
            'description': 'Введите название категории (например: Пиццы, Салаты, Напитки)'
        }),
        ('Статистика', {
            'fields': ['id'],
            'classes': ['collapse']  # Сворачиваемая секция
        }),
    ]

    def dishes_count(self, obj):

        count = obj.dishes.count()
        return f"📊 {count} блюд"

    dishes_count.short_description = 'Статистика'
    dishes_count.admin_order_field = 'dishes__count'  # Можно сортировать

    def view_dishes_link(self, obj):

        url = reverse('admin:catalog_dish_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">🔗 Посмотреть блюда</a>', url)

    view_dishes_link.short_description = 'Действия'

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'category', 'total_time',
        'is_available',
    ]

    search_fields = ['name', 'description', 'category__name']
    list_filter = ['category', 'is_available', 'prep_time', 'cooking_time']
    ordering = ['category__name', 'name']
    list_editable = ['is_available']
    list_per_page = 20
    list_display_links = ['id', 'name']
    actions = ['mark_as_available', 'mark_as_unavailable', 'increase_price_by_10_percent']

