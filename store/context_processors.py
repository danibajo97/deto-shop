from django.db.models import Max, Min

from .models import *


def get_prices(request):
    variations = Variation.objects.filter(is_active=True)
    price_min = Variation.objects.aggregate(Min('price'))
    price_max = Variation.objects.aggregate(Max('price'))
    min_price = price_min['price__min']
    max_price = price_max['price__max']
    for item in variations:
        if item.discount_price is not None and item.discount_price < min_price:
            min_price = round(item.discount_price, 0) - 1
    for item in variations:
        if item.discount_price is not None and item.discount_price > max_price:
            max_price = round(item.discount_price, 0)
    context = {
        'min_price': min_price,
        'max_price': max_price
    }
    return context


def get_variation_filters(request):
    size = Size.objects.all()
    color = Color.objects.all()
    context = {
        'size': size,
        'color': color
    }
    return context


def get_min_price():
    price_min = Variation.objects.aggregate(Min('price'))
    discount_price_min = Variation.objects.aggregate(Min('discount_price'))
    min_price = price_min['price__min']
    discount_min_price = discount_price_min['discount_price__min']
    if min_price < discount_min_price:
        return min_price
    else:
        return discount_min_price


def get_max_price():
    price_max = Variation.objects.aggregate(Max('price'))
    discount_price_max = Variation.objects.aggregate(Max('discount_price'))
    max_price = price_max['price__max']
    discount_max_price = discount_price_max['discount_price__max']
    if max_price > discount_max_price:
        return max_price
    else:
        return discount_max_price