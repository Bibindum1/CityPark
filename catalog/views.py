import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Order, OrderItem
from .models import Dish, Category
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'index.html')


def basket(request):
    return render(request, 'basket/basket.html')


def favourites(request):
    return render(request, 'basket/favourites.html')


def checkout(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        cart = data.get("cart", [])

        cart = [
            item for item in cart
            if item.get("name") and item.get("price") and str(item.get("price")).replace('.', '', 1).isdigit()
        ]

        if not cart:
            return JsonResponse({"status": "empty"})

        order = Order.objects.create(total=0)
        total = 0

        for item in cart:
            price = float(item["price"])
            qty = int(item.get("quantity", 1))

            total += price * qty

            OrderItem.objects.create(
                order=order,
                name=item["name"],
                price=price,
                quantity=qty
            )

        order.total = total
        order.save()

        return JsonResponse({
            "status": "ok",
            "order_id": order.id
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


def order_success(request, order_id):
    return render(request, "order_success.html", {
        "order_id": order_id
    })

def index(request):
    dishes = Dish.objects.filter(is_available=True)
    categories = Category.objects.all()
    return render(request, 'index.html', {'dishes': dishes, 'categories': categories})

@login_required
def profile(request):

    orders = Order.objects.all().order_by('-created_at')

    total_sum = sum(order.total for order in orders)
    avg_check = total_sum / len(orders) if orders else 0

    return render(request, 'profile.html', {
        'orders': orders,
        "total_sum": total_sum,
        "avg_check": avg_check,
    })

