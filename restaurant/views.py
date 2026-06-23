from django.shortcuts import render
from catalog.models import Dish, Category
from django.db.models import Q

from restaurant.models import Booking


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
        'query': query or "",
        'current_category': category or "all",
        'current_sort': sort or "",
    })


def wine_view(request):
    dishes = Dish.objects.filter(category__slug="wine")

    return render(request, 'wine.html', {
        'wines': dishes
    })


def booking_view(request):
    # ⚠️ сейчас заглушка — но безопасная
    if request.method == "POST":
        # тут пока нет модели бронирования в views → просто защита
        pass

    return render(request, 'booking.html')


def about_view(request):
    return render(request, 'about.html')


def contacts_view(request):
    return render(request, 'contacts.html')

from django.core.exceptions import ValidationError
def clean(self):
    exists = Booking.objects.filter(
        table=self.table,
        date=self.date,
        time=self.time
    ).exclude(pk=self.pk).exists()

    if exists:
        raise ValidationError("Этот стол уже занят на это время")