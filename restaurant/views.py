from django.shortcuts import render
from catalog.models import Dish, Category
from django.db.models import Q


def menu_view(request):
    dishes = Dish.objects.select_related('category').all()
    categories = Category.objects.all()

    # 🔎 ПОИСК
    query = request.GET.get('q')
    if query:
        dishes = dishes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # 🍽 ФИЛЬТР ПО КАТЕГОРИИ
    category = request.GET.get('category')
    if category and category != 'all':
        dishes = dishes.filter(category__name__iexact=category)

    # 🔃 СОРТИРОВКА
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        dishes = dishes.order_by('price')
    elif sort == 'price_desc':
        dishes = dishes.order_by('-price')
    elif sort == 'name':
        dishes = dishes.order_by('name')

    return render(request, 'menu.html', {
        'dishes': dishes,
        'categories': categories,
        'query': query,
        'current_category': category,
        'current_sort': sort,
    })


def booking_view(request):
    return render(request, 'booking.html')


def about_view(request):
    return render(request, 'about.html')


def contacts_view(request):
    return render(request, 'contacts.html')

def wine_view(request):
    dishes = Dish.objects.filter(category__name__iexact="Вино")
    return render(request, 'wine.html', {'wines': dishes})