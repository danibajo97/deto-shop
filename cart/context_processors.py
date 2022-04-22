from .calcule import *
from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                cart_count += item.quantity
        except Cart.DoesNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)


def cart_update(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart_items = CartItem.objects.filter(cart=cart[:1], is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
        except Cart.DoesNotExist:
            return {}
    return dict(cart_items=cart_items, total_paid=total_paid)
