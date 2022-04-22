from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('<slug:brand_slug>/', views.store, name='products_by_brand'),
    path('<slug:brand_slug>/<slug:category_slug>/<slug:product_slug>/', views.product_detail,
         name='product_detail'),
    path('<slug:brand_slug>/<slug:category_slug>/<slug:product_slug>/<slug:variation_slug>/', views.variation_detail,
         name='variation_detail'),
    path('search/', views.search, name='search'),
    path('submit-review/<int:product_id>', views.submit_review, name='submit_review'),
    path('add-wishlist', views.add_wishlist, name='add_wishlist'),
    # path('add-compare', views.add_compare, name='add_compare'),
    # path('remove-compare', views.remove_compare, name='remove_compare'),
    path('product-details/ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    path('product-details/ajaxprice/', views.ajaxprice, name='ajaxprice'),
]
