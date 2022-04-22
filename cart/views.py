from accounts.models import Account
from address.models import Address
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.generic.base import View
from orders.forms import *
from store.models import *
from store.models import Product, Variation

from .calcule import *
from .forms import *
from .models import *


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        print(cart)
    return cart


def add_cart(request, product_id):
    quantity = 0
    current_user = request.user
    print(product_id)
    product = Product.objects.get(id=product_id)
    # add to cart if the user is authenticated
    if current_user.is_authenticated:
        if product.variant == 'Size-Color':
            variation = None
            if request.method == 'POST':
                size_id = request.POST.get('size')
                size_selected = Size.objects.get(name=size_id)
                color_id = request.POST.get('color')
                color_selected = Color.objects.get(name=color_id)
                quantity = int(request.POST.get('quantity'))
                try:
                    variation = Variation.objects.get(product=product, color=color_selected, size=size_selected)
                except:
                    pass
            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user,
                                                          variations=variation).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, user=current_user, variations=variation)
                if cart_item.variations.stock >= (cart_item.quantity + quantity):
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    user=current_user
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})
        elif product.variant == 'Color':
            variation = None
            if request.method == 'POST':
                color_id = request.POST.get('color')
                color_selected = Color.objects.get(name=color_id)
                quantity = int(request.POST.get('quantity'))
                try:
                    variation = Variation.objects.get(product=product, color=color_selected)
                except:
                    pass
            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user,
                                                          variations=variation).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, user=current_user, variations=variation)
                if cart_item.variations.stock >= (cart_item.quantity + quantity):
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    user=current_user
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})
        elif product.variant == 'Size':
            variation = None
            if request.method == 'POST':
                size_id = request.POST.get('size')
                size_selected = Size.objects.get(name=size_id)
                quantity = int(request.POST.get('quantity'))
                try:
                    variation = Variation.objects.get(product=product, size=size_selected)
                except:
                    pass
            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user,
                                                          variations=variation).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, user=current_user, variations=variation)
                if cart_item.variations.stock >= (cart_item.quantity + quantity):
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    user=current_user
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})
        else:
            variation = None
            if request.method == 'POST':
                quantity = int(request.POST.get('quantity'))
                try:
                    variation = Variation.objects.filter(product=product).first()
                except:
                    pass
            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user,
                                                          variations=variation).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, user=current_user, variations=variation)
                if cart_item.variations.stock >= (cart_item.quantity + quantity):
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    user=current_user
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})


    # add to cart if user is not authenticated
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # busca o carrinho pela session da request
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        if product.variant == 'Size-Color':
            variation = None
            if request.method == 'POST':
                size_id = request.POST.get('size')
                size_selected = Size.objects.get(name=size_id)
                color_id = request.POST.get('color')
                color_selected = Color.objects.get(name=color_id)
                quantity = request.POST.get('quantity')
                try:
                    variation = Variation.objects.get(product=product, color=color_selected, size=size_selected)
                except:
                    pass

            is_cart_item_exists = CartItem.objects.filter(product=product, variations=variation, cart=cart).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, variations=variation, cart=cart)
                if cart_item.variations.stock >= (cart_item.quantity + int(quantity)):
                    cart_item.quantity += int(quantity)
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    cart=cart
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})
        elif product.variant == 'Color':
            variation = None
            if request.method == 'POST':
                color_id = request.POST.get('color')
                color_selected = Color.objects.get(name=color_id)
                quantity = int(request.POST.get('quantity'))
                try:
                    variation = Variation.objects.get(product=product, color=color_selected)
                except:
                    pass

            is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart,
                                                          variations=variation).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, cart=cart, variations=variation)
                if cart_item.variations.stock >= (cart_item.quantity + quantity):
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    cart=cart
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})
        elif product.variant == 'Size':
            variation = None
            if request.method == 'POST':
                size_id = request.POST.get('size')
                size_selected = Size.objects.get(name=size_id)
                quantity = int(request.POST.get('quantity'))
                try:
                    variation = Variation.objects.get(product=product, size=size_selected)
                except:
                    pass
            is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart,
                                                          variations=variation).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, cart=cart, variations=variation)
                if cart_item.variations.stock >= (cart_item.quantity + quantity):
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    cart=cart
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})
        else:
            variation = None
            if request.method == 'POST':
                quantity = int(request.POST.get('quantity'))
                try:
                    variation = Variation.objects.filter(product=product).first()
                except:
                    pass
            is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart,
                                                          variations=variation).exists()
            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product=product, cart=cart, variations=variation)
                if cart_item.variations.stock >= (cart_item.quantity + quantity):
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = cart_item.variations.stock
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    variations=variation,
                    quantity=quantity,
                    cart=cart
                )
                cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            total = 0
            quantity = 0
            total_paid = total_price(total, quantity, cart_items)
            cart_list = []
            for item in cart_items:
                cart_list.append(item)
            total_items = total_item(cart_items)
            context = {
                'total_paid': total_paid,
                'cart_items': cart_items
            }
            data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context)}
            return JsonResponse(
                {'total_items': total_items,
                 'data': data})


def remove_cart(request, cart_item_id):
    user = request.user
    if user.is_authenticated:
        if CartItem.objects.filter(user=user, id=cart_item_id).exists():
            cart_item = CartItem.objects.get(user=user, id=cart_item_id)
            cart_item.delete()
        total = 0
        quantity = 0
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        total_paid = total_price(total, quantity, cart_items)
        cart_list = []
        for item in cart_items:
            cart_list.append(item)
        total_items = total_item(cart_items)
        context = {
            'total_paid': total_paid,
            'cart_items': cart_items
        }
        data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context),
                'rendered_cart': render_to_string('store/shop-cart-info.html', context=context, request=request)
                }
        return JsonResponse(
            {'total_items': total_items,
             'data': data})
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        if CartItem.objects.filter(cart=cart, id=cart_item_id).exists():
            cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
            cart_item.delete()
        total = 0
        quantity = 0
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total_paid = total_price(total, quantity, cart_items)
        cart_list = []
        for item in cart_items:
            cart_list.append(item)
        total_items = total_item(cart_items)
        context = {
            'total_paid': total_paid,
            'cart_items': cart_items
        }
        data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context),
                'rendered_cart': render_to_string('store/shop-cart-info.html', context=context, request=request)
                }
        return JsonResponse(
            {'total_items': total_items,
             'data': data})


def remove_cart_item(request):
    user = request.user
    cart_id = request.GET.get('cart_id')
    if user.is_authenticated:
        if CartItem.objects.filter(user=user, id=cart_id).exists():
            cart_item = CartItem.objects.get(user=user, id=cart_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        total = 0
        quantity = 0
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        total_paid = total_price(total, quantity, cart_items)
        cart_list = []
        for item in cart_items:
            cart_list.append(item)
        total_items = total_item(cart_items)
        context = {
            'total_paid': total_paid,
            'cart_items': cart_items
        }
        data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context),
                'rendered_cart': render_to_string('store/shop-cart-info.html', context=context, request=request)
                }
        return JsonResponse(
            {'total_items': total_items,
             'data': data})
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        if CartItem.objects.filter(cart=cart, id=cart_id).exists():
            cart_item = CartItem.objects.get(cart=cart, id=cart_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        total = 0
        quantity = 0
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total_paid = total_price(total, quantity, cart_items)
        cart_list = []
        for item in cart_items:
            cart_list.append(item)
        total_items = total_item(cart_items)
        context = {
            'total_paid': total_paid,
            'cart_items': cart_items
        }
        data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context),
                'rendered_cart': render_to_string('store/shop-cart-info.html', context=context, request=request)
                }
        return JsonResponse(
            {'total_items': total_items,
             'data': data})


def add_cart_item(request):
    user = request.user
    cart_id = request.GET.get('cart_id')
    if user.is_authenticated:
        if CartItem.objects.filter(user=user, id=cart_id).exists():
            cart_item = CartItem.objects.get(user=user, id=cart_id)
            if cart_item.variations.stock >= (cart_item.quantity + 1):
                cart_item.quantity += 1
            else:
                cart_item.quantity = cart_item.variations.stock
            cart_item.save()
        total = 0
        quantity = 0
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        total_paid = total_price(total, quantity, cart_items)
        cart_list = []
        for item in cart_items:
            cart_list.append(item)
        total_items = total_item(cart_items)
        context = {
            'total_paid': total_paid,
            'cart_items': cart_items
        }
        data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context),
                'rendered_cart': render_to_string('store/shop-cart-info.html', context=context, request=request)
                }
        return JsonResponse(
            {'total_items': total_items,
             'data': data})
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        if CartItem.objects.filter(cart=cart, id=cart_id).exists():
            cart_item = CartItem.objects.get(cart=cart, id=cart_id)
            if cart_item.variations.stock >= (cart_item.quantity + 1):
                cart_item.quantity += 1
            else:
                cart_item.quantity = cart_item.variations.stock
            cart_item.save()
        total = 0
        quantity = 0
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total_paid = total_price(total, quantity, cart_items)
        cart_list = []
        for item in cart_items:
            cart_list.append(item)
        total_items = total_item(cart_items)
        context = {
            'total_paid': total_paid,
            'cart_items': cart_items
        }
        data = {'rendered_table': render_to_string('includes/mini-cart.html', context=context),
                'rendered_cart': render_to_string('store/shop-cart-info.html', context=context, request=request)
                }
        return JsonResponse(
            {'total_items': total_items,
             'data': data})


def cart(request, total=0, quantity=0, cart_items=None):
    title = 'Cart'
    total_paid = 0
    total_items = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total_paid = total_price(total, quantity, cart_items)
        total_items = total_item(cart_items)
    except ObjectDoesNotExist:
        pass
    context = {
        'title': title,
        'total_items': total_items,
        'cart_items': cart_items,
        'total_paid': total_paid
    }
    return render(request, 'store/shop-cart.html', context)


def checkout(request, total=0, quantity=0, cart_items=None):
    paymentForm = PaymentForm()
    couponForm = CouponForm()
    # refundForm = RefundForm()
    context = {}
    grand_total = 0
    coupon = 0
    try:
        if request.user.is_authenticated:
            user = Account.objects.get(id=request.user.id)
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            userAddress = Address.objects.filter(user=request.user)
            userAddressActive = 0
            for active in userAddress:
                if active.status:
                    userAddressActive = active
            if userAddressActive:
                orderUserForm = OrderUserForm(instance=user)
                orderAddressForm = OrderAddressForm(instance=userAddressActive)
            else:
                orderUserForm = OrderUserForm(instance=user)
                orderAddressForm = OrderAddressForm()
            context.update({
                'orderUserForm': orderUserForm,
                'orderAddressForm': orderAddressForm,
            })
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            orderAddressForm = OrderAddressForm()
            orderVisitorsForm = OrderVisitorsForm()
            context.update({
                'orderVisitorsForm': orderVisitorsForm,
                'orderAddressForm': orderAddressForm,
            })
        for item in cart_items:
            if item.variations.discount_price:
                total += round((item.variations.discount_price * item.quantity), 2)
                quantity += item.quantity
            else:
                total += round((item.variations.price * item.quantity), 2)
                quantity += item.quantity
            if item.coupon:
                coupon = item.coupon.amount
        grand_total = round(total, 2)
        if coupon != 0:
            grand_total = float(grand_total) - coupon
            grand_total = round(grand_total, 2)

    except ObjectDoesNotExist:
        pass

    context.update({
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "paymentForm": paymentForm,
        "grand_total": grand_total,
        "couponForm": couponForm,
    })
    return render(request, 'store/checkout.html', context)


