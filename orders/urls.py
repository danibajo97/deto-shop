from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('add_coupon/', AddCouponView.as_view(), name='add-coupon'),
    # path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
]
