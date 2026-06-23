from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages

from catalog.models import Dish, Category
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
    wines = Dish.objects.filter(category__slug="wine")

    return render(request, 'wine.html', {
        'wines': wines
    })


def booking_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")
        guests = request.POST.get("guests", 1)

        exists = Booking.objects.filter(
            booking_date=booking_date,
            booking_time=booking_time
        ).exists()

        if exists:
            messages.error(request, "Это время уже занято")
        else:
            Booking.objects.create(
                full_name=full_name,
                phone=phone,
                email=email,
                booking_date=booking_date,
                booking_time=booking_time,
                guests=guests
            )
            messages.success(request, "Бронирование создано")

        return redirect("booking")

    return render(request, "booking.html")


def about_view(request):
    return render(request, "about.html")


def contacts_view(request):
    return render(request, "contacts.html")