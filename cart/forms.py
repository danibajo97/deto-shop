from django import forms
from django.forms import fields

from .models import *


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('code',)

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = 'Coupon Code'
