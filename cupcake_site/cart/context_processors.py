from .models import Cart

def cart_quantity(request):
    if request.user.is_authenticated:
        total_qty = sum(
            item.quantity for item in Cart.objects.filter(user=request.user)
        )
    else:
        total_qty = 0

    return {
        'cart_quantity': total_qty
    }
