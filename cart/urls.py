from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/', views.remove_cart_item, name='remove_cart_item'),
    path('add_cart_item/', views.add_cart_item, name='add_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
]
