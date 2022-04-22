from django.shortcuts import render
from store.models import *
from category.models import Category
from brand.models import Brand
from .models import Slides
from newsletter.models import Blog


def home(request):
    products = Product.objects.filter(is_available=True).order_by('-updated_at')
    categories = Category.objects.filter(is_active=True)[0:8]
    latest_blogs = Blog.objects.filter(is_active=True)[0:2]
    brands = Brand.objects.filter(is_active=True)
    slides = Slides.objects.filter(is_active=True)
    title = "home"

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
        'categories': categories,
        'latest_blogs': latest_blogs,
        'brands': brands,
        'slides': slides,
        'title': title
    }
    return render(request, 'home.html', context)
