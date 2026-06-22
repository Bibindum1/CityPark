from django.shortcuts import render
from catalog.models import Dish, Category

def menu_view(request):
    dishes = Dish.objects.all()
    categories = Category.objects.all()
    return render(request, 'menu.html', {
        'dishes': dishes,
        'categories': categories
    })

def booking_view(request):
    return render(request, 'booking.html')

def about_view(request):
    return render(request, 'about.html')

def wine_view(request):
    wines = Dish.objects.filter(category__name='Вино')
    return render(request, 'wine.html', {'wines': wines})

def contacts_view(request):
    return render(request, 'contacts.html')