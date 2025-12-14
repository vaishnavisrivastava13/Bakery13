from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order

def order_page(request):
    cart = request.session.get("cart", [])

    total_price = sum(item["price"] * item.get("qty", 1) for item in cart)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            cart_items=str(cart),
            total_price=0,  # You can update with real prices later
            payment_method="COD",
        )

        request.session["cart"] = []   # clear cart
        return render(request, "order_success.html", {"order": order})

    return render(request, "order.html", {"cart": cart, "total": total_price})
