import datetime
import json

from insomnio import settings
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from address.models import Address
from cart.models import CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic.base import View
from store.models import Product
from cart.models import Cart, Coupon
from cart.views import _cart_id
from .forms import *
from cart.forms import *
from .models import *


def place_order(request, total=0, quantity=0):
    if request.method == 'POST':
        if request.user.is_authenticated:
            current_user = request.user
            cart_items = CartItem.objects.filter(user=current_user)
            cart_count = cart_items.count()

            if cart_count < 1:
                return redirect('store')

            coupon = 0
            used_coupon = None

            for item in cart_items:
                if item.variations.discount_price:
                    total += round((item.variations.discount_price * item.quantity), 2)
                    quantity += item.quantity
                    if item.coupon:
                        coupon = item.coupon.amount
                        used_coupon = Coupon.objects.get(id=item.coupon.id)
                else:
                    total += round((item.variations.price * item.quantity), 2)
                    quantity += item.quantity
                    if item.coupon:
                        coupon = item.coupon.amount
                        used_coupon = Coupon.objects.get(id=item.coupon.id)

            grand_total = round(total, 2)
            if coupon is not 0:
                grand_total = float(grand_total) - coupon
                grand_total = round(grand_total, 2)

            checkoutData = OrderAddressForm(request.POST)
            userAddress = Address.objects.filter(user=current_user)
            existAddress = 1
            if userAddress:
                for address in userAddress:
                    if address.street_address == \
                            checkoutData.data['street_address'] and address.apartment_address == \
                            checkoutData.data['apartment_address'] and address.city == \
                            checkoutData.data['city'] and address.state == \
                            checkoutData.data['state'] and address.country == \
                            checkoutData.data['country']:
                        existAddress = 0
                    else:
                        existAddress = 1
            if checkoutData.is_valid() and existAddress == 1:
                address = Address.objects.filter(user=current_user)
                if address:
                    for address in address:
                        address.status = False
                        address.save()
                saveForm = checkoutData.save(commit=False)
                saveForm.user = request.user
                saveForm.status = True
                saveForm.save()
            if checkoutData.is_valid():
                address = Address.objects.get(user=request.user, status=True)
                data = Order()
                data.user = current_user
                if request.POST.get('order_notes'):
                    data.order_note = request.POST.get('order_notes')
                data.shipping_address = address
                data.order_total = grand_total
                data.save()
                year = int(datetime.date.today().strftime('%Y'))
                month = int(datetime.date.today().strftime('%m'))
                day = int(datetime.date.today().strftime('%d'))
                d = datetime.date(year, month, day)
                current_date = d.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()

                order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
                payment_id = current_date + str(order_number)
                payment = Payment(
                    user=request.user,
                    payment_id=payment_id,
                    payment_method=request.POST['payment_method'],
                    total_paid=grand_total,
                    status=order.status,
                )
                payment.save()
                order.payment = payment
                order.is_ordered = True
                order.save()

                for item in cart_items:
                    order_product = OrderProduct()
                    order_product.order = order
                    order_product.user = request.user
                    order_product.product = item.product
                    order_product.quantity = item.quantity
                    order_product.variations = item.variations
                    order_product.ordered = True
                    order_product.save()

                    variation = Variation.objects.get(id=item.variations.id)
                    if variation.stock - item.quantity == 0:
                        variation.is_active = False
                    else:
                        variation.stock -= item.quantity
                    variation.save()

                CartItem.objects.filter(user=request.user).delete()
                ordered_products = OrderProduct.objects.filter(order=order)

                mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                mailServer.starttls()
                mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                email_to = request.user.email
                message = MIMEMultipart()
                message['From'] = settings.EMAIL_HOST_USER
                message['To'] = email_to
                message['Subject'] = 'Thank you for your order'

                content = render_to_string('orders/order_received_email.html', {
                    'user': request.user,
                    'order': order,
                    'ordered_products': ordered_products,
                })
                message.attach(MIMEText(content, 'html'))

                mailServer.sendmail(settings.EMAIL_HOST_USER,
                                    email_to,
                                    message.as_string())

                payment = Payment.objects.get(payment_id=payment_id)

                try:
                    order = Order.objects.get(order_number=order_number, is_ordered=True)
                    ordered_products = OrderProduct.objects.filter(order=order)
                    context = {
                        'order': order,
                        'used_coupon': used_coupon,
                        'ordered_products': ordered_products,
                        'order_number': order.order_number,
                        'transactionID': payment.payment_id,
                        'payment': payment,
                        'grand_total': grand_total,
                    }
                    if used_coupon:
                        used_coupon.delete()
                    return render(request, 'orders/order_completed.html', context)
                except (Payment.DoesNotExist, Order.DoesNotExist):
                    return redirect('home')
            else:
                messages.error(request, 'Invalid inputs!')
                return redirect('checkout')

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            cart_count = cart_items.count()

            if cart_count < 1:
                return redirect('store')

            coupon = 0
            for item in cart_items:
                if item.variations.discount_price:
                    total += round((item.variations.discount_price * item.quantity), 2)
                    quantity += item.quantity
                    if item.coupon:
                        coupon = item.coupon.amount
                        Coupon.objects.get
                else:
                    total += round((item.variations.price * item.quantity), 2)
                    quantity += item.quantity
                    if item.coupon:
                        coupon = item.coupon.amount

            grand_total = round(total, 2)
            if coupon is not 0:
                grand_total = float(grand_total) - coupon
                grand_total = round(grand_total, 2)

            checkoutVisitorsData = OrderVisitorsForm(request.POST)
            checkoutAddressData = OrderAddressForm(request.POST)
            if checkoutAddressData.is_valid() and checkoutVisitorsData.is_valid():
                saveVisitorsForm = checkoutVisitorsData.save(commit=False)
                saveVisitorsForm.save()
                user = Account.objects.get(email=request.POST.get('email'))
                user.is_visitor = True
                user.save()
                saveAddressForm = checkoutAddressData.save(commit=False)
                saveAddressForm.user = user
                saveAddressForm.save()
                address = Address.objects.get(user=user)
                data = Order()
                data.user = user
                if request.POST.get('order_note'):
                    data.order_note = request.POST.get('order_note')
                data.shipping_address = address
                data.order_total = grand_total
                data.save()
                year = int(datetime.date.today().strftime('%Y'))
                month = int(datetime.date.today().strftime('%m'))
                day = int(datetime.date.today().strftime('%d'))
                d = datetime.date(year, month, day)
                current_date = d.strftime("%Y%m%d")
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()

                order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
                payment_id = current_date + str(order_number)
                payment = Payment(
                    user=user,
                    payment_id=payment_id,
                    payment_method=request.POST['payment_method'],
                    total_paid=grand_total,
                    status=order.status,
                )
                payment.save()
                order.payment = payment
                order.is_ordered = True
                order.save()

                for item in cart_items:
                    order_product = OrderProduct()
                    order_product.order = order
                    order_product.user = user
                    order_product.product = item.product
                    order_product.quantity = item.quantity
                    order_product.variations = item.variations
                    order_product.ordered = True
                    order_product.save()

                    variation = Variation.objects.get(id=item.variations.id)
                    if variation.stock - item.quantity == 0:
                        variation.is_active = False
                    else:
                        variation.stock -= item.quantity
                    variation.save()


                CartItem.objects.filter(cart=cart).delete()
                ordered_products = OrderProduct.objects.filter(order=order)

                mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                mailServer.starttls()
                mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                email_to = request.user.email
                message = MIMEMultipart()
                message['From'] = settings.EMAIL_HOST_USER
                message['To'] = email_to
                message['Subject'] = 'Thank you for your order'

                content = render_to_string('orders/order_received_email.html', {
                    'user': user,
                    'order': order,
                    'ordered_products': ordered_products,
                })
                message.attach(MIMEText(content, 'html'))

                mailServer.sendmail(settings.EMAIL_HOST_USER,
                                    email_to,
                                    message.as_string())

                payment = Payment.objects.get(payment_id=payment_id)

                try:
                    order = Order.objects.get(order_number=order_number, is_ordered=True)
                    ordered_products = OrderProduct.objects.filter(order=order)

                    context = {
                        'order': order,
                        'ordered_products': ordered_products,
                        'order_number': order.order_number,
                        'transactionID': payment.payment_id,
                        'payment': payment,
                        'grand_total': grand_total,
                    }
                    return render(request, 'orders/order_completed.html', context)
                except (Payment.DoesNotExist, Order.DoesNotExist):
                    return redirect('home')
            else:
                messages.error(request, 'Invalid inputs!')
                return redirect('checkout')


# class RequestRefundView(View):
#     def get(self, *args, **kwargs):
#         form = RefundForm()
#         context = {
#             'form': form
#         }
#         return render(self.request, "request_refund.html", context)
# 
#     def post(self, *args, **kwargs):
#         form = RefundForm(self.request.POST)
#         if form.is_valid():
#             ref_code = form.cleaned_data.get('ref_code')
#             message = form.cleaned_data.get('message')
#             email = form.cleaned_data.get('email')
#             # edit the order
#             try:
#                 order = Order.objects.get(ref_code=ref_code)
#                 order.refund_requested = True
#                 order.save()
# 
#                 # store the refund
#                 refund = Refund()
#                 refund.order = order
#                 refund.reason = message
#                 refund.email = email
#                 refund.save()
# 
#                 messages.info(self.request, "Your request was received")
#                 return redirect("request-refund")
# 
#             except ObjectDoesNotExist:
#                 messages.info(self.request, "This order does not exist")
#                 return redirect("request-refund")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                carCoupon = CartItem.objects.filter(user=self.request.user, is_active=True)
                carCoupon = carCoupon.first()
                try:
                    coupon = Coupon.objects.get(code=code)
                except ObjectDoesNotExist:
                    messages.info(self.request, "This coupon does not exist")
                    return redirect("checkout")
                carCoupon.coupon = coupon
                carCoupon.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")
