
from django.shortcuts import render
from django.db.models import Q

from catalog.models import Dish, Category


def menu_view(request):
    dishes = Dish.objects.select_related('category').all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        dishes = dishes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    category = request.GET.get('category')
    if category and category != 'all':
        dishes = dishes.filter(category__slug=category)

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
        'category': category,
        'sort': sort,
    })


def booking_view(request):
    return render(request, 'booking.html')


def about_view(request):
    return render(request, 'about.html')


def wine_view(request):
    return render(request, 'wine.html')


def contacts_view(request):
    return render(request, 'contacts.html')
