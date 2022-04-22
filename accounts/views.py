import calendar
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from address.models import Address
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, message
from django.db.models import Count
# verification email
from django.db.models.functions import ExtractMonth, datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from insomnio import settings
from orders.models import Order, OrderProduct
from store.models import Wishlist, ReviewRating

from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account


# Create your views here.
# @csrf_exempt
def register(request):
    title = 'register'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               password=password)
            user.save()

            current_site = get_current_site(request)
            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = user.email
            message = MIMEMultipart()
            message['From'] = settings.EMAIL_HOST_USER
            message['To'] = email_to
            message['Subject'] = 'Account Activation Message'

            content = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            message.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                message.as_string())
            messages.success(request,
                             'Thank you for registering with us. we have sent you a verification email to your email address. Please verify it.')
            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
        context = {
            'form': form,
            'title': title
        }
    return render(request, 'accounts/register.html', context)


def login(request):
    title = 'login'
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart items from the user to access is product variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # print('Query ->', query)
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                # print('Params ->', params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')

        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html', context={'title': title})


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('home')
    return


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        messages.success(request, 'Congrulations! your account is activated.')
        return redirect('home')
    else:
        message.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    title = 'Dashboard'
    orders = Order.objects.order_by("-created_at").filter(user=request.user, is_ordered=True)
    orders_count = orders.count()

    orders = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(
        count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])

    # Get for Filter
    userprofile = Account.objects.filter(id=request.user.id)
    context = {
        'monthNumber': monthNumber,
        'totalOrders': totalOrders,
        'orders_count': orders_count,
        'userprofile': userprofile,
        'title': title,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    title = 'ForgotPassword'
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = email
            message = MIMEMultipart()
            message['From'] = settings.EMAIL_HOST_USER
            message['To'] = email_to
            message['Subject'] = 'Reset your password'

            content = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            message.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                message.as_string())
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html', {'title': title})


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def my_orders(request):
    title = 'My Orders'
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
        'title': title,
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def my_wishlist(request):
    title = 'My Wishlist'
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    products = []
    for wsl in wlist:
        products.append(wsl.product)

    context = {
        'products': products,
        'title': title
    }
    return render(request, 'accounts/wishlist.html', context)


@login_required(login_url='login')
def my_reviews(request):
    reviews = ReviewRating.objects.filter(user=request.user).order_by('-id')
    title = 'Reviews'
    context = {'reviews': reviews,
               'title': title}
    return render(request, 'accounts/reviews.html', context)


@login_required(login_url='login')
def edit_profile(request):
    title = 'Edit Profile'
    picture_profile = get_object_or_404(Account, email=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        context = {
            'user_form': user_form,
            'picture_profile': picture_profile,
            'title': title,
        }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    title = 'Change Password'
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html', {'title': title})


@login_required(login_url='login')
def order_detail(request, order_id):
    title = 'Order Detail'
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    grand_total = order.order_total

    context = {
        'order_detail': order_detail,
        'order': order,
        'title': title,
        'grand_total': grand_total,
    }
    return render(request, 'accounts/order_detail.html', context)

# @login_required(login_url='login')
# def compare(request):
#     title = 'Compare'
#     compare_products = CompareProducts.objects.filter(user=request.user).order_by('-id')
#     products = []
#     for product in compare_products:
#         products.append(product.product)
# 
#     context = {
#         'products': products,
#         'title': title
#     }
#     return render(request, 'accounts/compare.html', context)
