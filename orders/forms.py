from accounts.models import Account
from address.models import Address
from django import forms
from django.forms import fields
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from orders.models import *


class OrderAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('phone_number', 'street_address', 'apartment_address',
                  'city', 'state', 'country', 'zip', 'note_address')

    def __init__(self, *args, **kwargs):
        super(OrderAddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class OrderUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(OrderUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].disabled = True


class OrderVisitorsForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(OrderVisitorsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# class RefundForm(forms.ModelForm):
#     class Meta:
#         model = Refund
#         fields = ('order', 'reason', 'email')


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment_method',)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].widget.attrs['class'] = 'form-control'
        self.fields['payment_method'].label = ""
