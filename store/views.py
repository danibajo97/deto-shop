import re

from brand.models import Brand
from cart.calcule import *
from cart.models import Cart, CartItem
from cart.views import _cart_id
from category.models import Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Max, Min, Count, Avg, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from orders.models import OrderProduct

from .forms import ReviewForm
from .models import *


def store(request, category_slug=None, brand_slug=None):
    context = {}
    product_count = 0
    max = 0
    min = 0
    colors = []
    sizes = []
    final_products = []
    final_price_products = []
    flag = 0
    selected = ""
    if request.GET.get('selected'):
        selected = request.GET.get('selected')
    if request.GET.get('filter'):
        filter = request.GET.get('filter')
        max, min = max_min_values(filter)
    if request.GET.get('colorlist'):
        colors_list = request.GET.get('colorlist')
        colors = [float(s) for s in re.findall(r'-?\d+\.?\d*', colors_list)]
    if request.GET.get('sizelist'):
        sizes_list = request.GET.get('sizelist')
        sizes = [float(s) for s in re.findall(r'-?\d+\.?\d*', sizes_list)]
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        if selected == "D-N":
            products = Product.objects.filter(category=categories, is_available=True, ).order_by("-updated_at")
        elif selected == "D-O":
            products = Product.objects.filter(category=categories, is_available=True, ).order_by("updated_at")
        elif selected == "A-Z":
            products = Product.objects.filter(category=categories, is_available=True, ).order_by("name")
        elif selected == "Z-A":
            products = Product.objects.filter(category=categories, is_available=True, ).order_by("-name")
        elif selected == "sort":
            products = Product.objects.filter(category=categories, is_available=True, ).order_by("id")
        else:
            products = Product.objects.filter(category=categories, is_available=True, )

        if max and min:
            for p_item in products:
                variations = p_item.get_variation_all()
                final_list = filter_price_products(variations, max, min)
                for variation in final_list:
                    if variation.product not in final_price_products:
                        final_price_products.append(variation.product)

            for p_item in final_price_products:
                variations = p_item.get_variation_all()
                if len(colors) > 0 and len(sizes) > 0:
                    flag = 1
                    final_list = find_colors(variations, colors)
                    final_list = find_sizes(final_list, sizes)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)
                elif len(sizes) > 0 and len(colors) == 0:
                    flag = 1
                    final_list = find_sizes(variations, sizes)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)
                elif len(sizes) == 0 and len(colors) > 0:
                    flag = 1
                    final_list = find_colors(variations, colors)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)

        if len(final_products) > 0:
            paginator = Paginator(final_products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(final_products)
        elif len(final_price_products) > 0 and len(final_products) == 0 and flag == 1:
            paged_products = None
        elif len(final_price_products) > 0 and len(final_products) == 0 and flag == 0:
            paginator = Paginator(final_price_products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(final_price_products)
        else:
            paginator = Paginator(products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(products)
        title = "Categories"
        context.update({'categories': categories})
    elif brand_slug is not None:
        brands = get_object_or_404(Brand, slug=brand_slug)
        if selected == "D-N":
            products = Product.objects.filter(brand=brands, is_available=True, ).order_by("-updated_at")
        elif selected == "D-O":
            products = Product.objects.filter(brand=brands, is_available=True, ).order_by("updated_at")
        elif selected == "A-Z":
            products = Product.objects.filter(brand=brands, is_available=True, ).order_by("name")
        elif selected == "Z-A":
            products = Product.objects.filter(brand=brands, is_available=True, ).order_by("-name")
        elif selected == "sort":
            products = Product.objects.filter(brand=brands, is_available=True, ).order_by("id")
        else:
            products = Product.objects.filter(brand=brands, is_available=True, )

        if max and min:
            for p_item in products:
                variations = p_item.get_variation_all()
                final_list = filter_price_products(variations, max, min)
                for variation in final_list:
                    if variation.product not in final_price_products:
                        final_price_products.append(variation.product)

            for p_item in final_price_products:
                variations = p_item.get_variation_all()
                if len(colors) > 0 and len(sizes) > 0:
                    flag = 1
                    final_list = find_colors(variations, colors)
                    final_list = find_sizes(final_list, sizes)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)
                elif len(sizes) > 0 and len(colors) == 0:
                    flag = 1
                    final_list = find_sizes(variations, sizes)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)
                elif len(sizes) == 0 and len(colors) > 0:
                    flag = 1
                    final_list = find_colors(variations, colors)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)

        if len(final_products) > 0:
            paginator = Paginator(final_products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(final_products)
        elif len(final_price_products) > 0 and len(final_products) == 0 and flag == 1:
            paged_products = None
        elif len(final_price_products) > 0 and len(final_products) == 0 and flag == 0:
            paginator = Paginator(final_price_products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(final_price_products)
        else:
            paginator = Paginator(products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(products)
        title = "Brands"
        context.update({'brands': brands})
    else:
        if selected == "D-N":
            products = Product.objects.filter(is_available=True, ).order_by("-updated_at")
        elif selected == "D-O":
            products = Product.objects.filter(is_available=True, ).order_by("updated_at")
        elif selected == "A-Z":
            products = Product.objects.filter(is_available=True, ).order_by("name")
        elif selected == "Z-A":
            products = Product.objects.filter(is_available=True, ).order_by("-name")
        elif selected == "sort":
            products = Product.objects.filter(is_available=True, ).order_by("id")
        else:
            products = Product.objects.filter(is_available=True).order_by("-id")
        if max and min:
            for p_item in products:
                variations = p_item.get_variation_all()
                final_list = filter_price_products(variations, max, min)
                for variation in final_list:
                    if variation.product not in final_price_products:
                        final_price_products.append(variation.product)

            for p_item in final_price_products:
                variations = p_item.get_variation_all()
                if len(colors) > 0 and len(sizes) > 0:
                    flag = 1
                    final_list = find_colors(variations, colors)
                    final_list = find_sizes(final_list, sizes)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)
                elif len(sizes) > 0 and len(colors) == 0:
                    flag = 1
                    final_list = find_sizes(variations, sizes)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)
                elif len(sizes) == 0 and len(colors) > 0:
                    flag = 1
                    final_list = find_colors(variations, colors)
                    for variation in final_list:
                        if variation.product not in final_products:
                            final_products.append(variation.product)

        if len(final_products) > 0:
            paginator = Paginator(final_products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(final_products)
        elif len(final_price_products) > 0 and len(final_products) == 0 and flag == 1:
            paged_products = None
        elif len(final_price_products) > 0 and len(final_products) == 0 and flag == 0:
            paginator = Paginator(final_price_products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(final_price_products)
        else:
            paginator = Paginator(products, 16)
            page = request.GET.get('page')
            if page:
                page = int(page)
            paged_products = paginator.get_page(page)
            product_count = len(products)
        title = "Store"
    popular_products = Variation.objects.filter(label="hot", is_active=True)
    if request.user.is_authenticated:
        context.update({
            'user': request.user
        })
    context.update({'products': paged_products,
                    'popular_products': popular_products,
                    'title': title,
                    'product_count': product_count,
                    })
    if request.GET.get('listid') == "2":
        data = {'rendered_store': render_to_string('store/shop-listview.html', context=context)}
        return JsonResponse(data)
    elif request.GET.get('listid') == "1":
        data = {'rendered_store': render_to_string('store/shop-gridview.html', context=context)}
        return JsonResponse(data)
    else:
        return render(request, 'store/shop.html', context)


def product_detail(request, brand_slug, category_slug, product_slug):
    title = 'Product Detail'
    context = {}
    try:
        single_product = Product.objects.get(brand__slug=brand_slug, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product=single_product).exists()
        except CartItem.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product=single_product, status=True)
    reviews_count = reviews.count()
    related_products = Product.objects.filter(category=single_product.category, is_available=True).exclude(
        id=single_product.id)[0:5]
    context.update({
        'product': single_product,
        'related_products': related_products,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'title': title,
        'reviews_count': reviews_count,
    })
    if single_product.variant != "None":  # Product have variants
        variant = single_product.get_variation()
        size = variant.size
        variations = Variation.objects.filter(product=single_product, size=size, is_active=True)
        context.update({
            'variant': variant,
            'variations': variations,
        })

    return render(request, 'store/product-details.html', context)


def variation_detail(request, brand_slug, category_slug, product_slug, variation_slug):
    title = 'Product Detail'
    context = {}
    try:
        single_product = Product.objects.get(brand__slug=brand_slug, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product=single_product).exists()
        except CartItem.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product=single_product, status=True)
    reviews_count = reviews.count()
    related_products = Product.objects.filter(category=single_product.category, is_available=True).exclude(
        id=single_product.id)[0:5]
    context.update({
        'product': single_product,
        'related_products': related_products,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'title': title,
        'reviews_count': reviews_count,
    })
    if single_product.variant != "None":  # Product have variants
        variant = None
        variations = Variation.objects.filter(product=single_product)
        for item in variations:
            if item.slug == variation_slug:
                variant = Variation.objects.get(id=item.id)
        size = variant.size
        variations = Variation.objects.filter(product=single_product, size=size, is_active=True)
        context.update({
            'variant': variant,
            'variations': variations,
        })

    return render(request, 'store/product-details.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        size_selected = Size.objects.get(name=size_id)
        productid = request.POST.get('productid')
        products = Variation.objects.filter(product=productid, size=size_selected.id, is_active=True)
        if request.POST.get('color'):
            color_id = request.POST.get('color')
            color_selected = Color.objects.get(name=color_id)
            try:
                variant = products.get(product=productid, color=color_selected, is_active=True)
            except:
                variant = products.first()
        else:
            variant = products.first()
        context = {
            'size_id': size_selected.id,
            'productid': productid,
            'products': products,
            'variant': variant,
            'size_selected': size_selected,
        }
        data = {'rendered_table': render_to_string('store/color-list.html', context=context, request=request),
                'rendered_gallery': render_to_string('store/gallery-info.html', context={'product': variant},
                                                     request=request),
                'rendered_info': render_to_string('store/product-info.html', context={'product': variant},
                                                  request=request)
                }
        return JsonResponse(data)
    return JsonResponse(data)


def ajaxprice(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        productid = request.POST.get('productid')
        if size_id is not None and color_id is not None:
            size_selected = Size.objects.get(name=size_id)
            color_selected = Color.objects.get(name=color_id)
            product = Variation.objects.get(product=productid, size=size_selected, color=color_selected,
                                            is_active=True)
        elif color_id is not None and size_id is None:
            color_id = request.POST.get('color')
            color_selected = Color.objects.get(name=color_id)
            product = Variation.objects.filter(product=productid, color=color_selected, is_active=True).first()
        else:
            size_id = request.POST.get('size')
            size_selected = Size.objects.get(name=size_id)
            product = Variation.objects.filter(product=productid, size=size_selected, is_active=True).first()
        context = {
            'product': product,
        }
        data = {'rendered_table': render_to_string('store/product-info.html', context=context, request=request),
                'rendered_gallery': render_to_string('store/gallery-info.html', context=context, request=request),
                'rendered_quick_gallery': render_to_string('includes/quick-color.html', context=context,
                                                           request=request)
                }
        return JsonResponse(data)
    return JsonResponse(data)


def search(request):
    products = {}
    if 'q' in request.GET:
        keyword = request.GET['q']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword)
                                                                      | Q(name__icontains=keyword))
    context = {
        'products': products,
    }
    return render(request, 'store/search-result.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    try:
        review = ReviewRating.objects.get(user=request.user, product=product)
        form = ReviewForm(request.POST, instance=review)
        # updated_at
        form.save()
        messages.success(request, 'Review updated.')
        return redirect(url)

    except ReviewRating.DoesNotExist:
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = ReviewRating()
            data.subject = form.cleaned_data['subject']
            data.review = form.cleaned_data['review']
            data.rating = form.cleaned_data['rating']
            # created_at
            data.product = product
            data.user = request.user
            data.save()
            messages.success(request, 'Review created.')
            return redirect(url)
        else:
            messages.error(request, 'Ups! Something was wrong, try later.')
            return redirect(url)


# Wishlist
def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    exists_product = Wishlist.objects.filter(product=product, user=request.user)
    if exists_product:
        exists_product.delete()
        data = {
            'bool': False,
        }
    else:
        product = Wishlist(
            product=product,
            user=request.user
        )
        product.save()
        data = {
            'bool': True,
        }
    return JsonResponse(data)

# def add_compare(request):
#     pid = request.GET['product']
#     product = Product.objects.get(pk=pid)
#     exists_product = CompareProducts.objects.filter(product=product, user=request.user)
#     if exists_product:
#         data = {
#             'bool': False,
#         }
#     else:
#         product = CompareProducts(
#             product=product,
#             user=request.user
#         )
#         product.save()
#         data = {
#             'bool': True,
#         }
#     return JsonResponse(data)
# 
# 
# def remove_compare(request):
#     pid = request.GET['product']
#     product = Product.objects.get(pk=pid)
#     exists_product = CompareProducts.objects.get(product=product, user=request.user)
#     exists_product.delete()
#     compare_products = CompareProducts.objects.filter(user=request.user).order_by('-id')
#     products = []
#     for product in compare_products:
#         products.append(product.product)
#     context = {
#         'products': products
#     }
#     print(products)
#     data = {'rendered_table': render_to_string('accounts/compare-table.html', context=context, request=request),
#             }
#     return JsonResponse(data)
