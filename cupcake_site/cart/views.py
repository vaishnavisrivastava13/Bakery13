from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Cart,DeliveryAddress
from .forms import CheckoutForm
import json

@login_required
def add_to_cart(request, model_name, product_id):

    MODEL_MAP = {
        "cake": ("cakes", "cake"),
        "cupcake": ("cupcakes", "cupcake"),
        "dessert": ("dessert", "dessert"),
        "beverage": ("beverages", "beverage"),
        "gift": ("gift", "gift"),
    }

    if model_name not in MODEL_MAP:
        return redirect("cart")

    app_label, model = MODEL_MAP[model_name]

    content_type = ContentType.objects.get(
        app_label=app_label,
        model=model
    )

    product = get_object_or_404(
        content_type.model_class(),
        id=product_id
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=product.id,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'cart'))

@login_required
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate subtotal and each item total
    for item in cart_items:
        item.item_total = item.product.price * item.quantity

    subtotal = sum(item.item_total for item in cart_items)
    gst = round(subtotal * 0.05)   # 5% GST
    delivery_charge = 40 if subtotal > 0 else 0
    total = subtotal + gst + delivery_charge
    address_obj = DeliveryAddress.objects.filter(user=request.user).first()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'gst': gst,
        'delivery_charge': delivery_charge,
        'total': total,
        'saved_address': address_obj.address if address_obj else ''
    })


@login_required
def save_address(request):
    if request.method == "POST":
        address = request.POST.get("address")

        DeliveryAddress.objects.update_or_create(user=request.user, defaults={'address': address})

    return redirect('cart')

@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)

        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()

        # Recalculate totals
        cart_items = Cart.objects.filter(user=request.user)
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        gst = round(subtotal * 0.05)
        delivery_charge = 40 if subtotal > 0 else 0
        total = subtotal + gst + delivery_charge

        item_total = cart_item.product.price * cart_item.quantity

        return JsonResponse({
            'quantity': cart_item.quantity,
            'item_total': item_total,
            'subtotal': subtotal,
            'gst': gst,
            'delivery_charge': delivery_charge,
            'total': total
        })

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    summary_items = []
    total_price = 0

    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_price += item_total

        summary_items.append({
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'total': item_total
        })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Clear cart after order
            cart_items.delete()
            return redirect('order_success')
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'cart_items': summary_items,
        'total_price': total_price,
        'form': form
    })


@login_required
def order_success(request):
    return render(request, 'order_success.html')
