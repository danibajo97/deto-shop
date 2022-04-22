from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone_number',
        'street_address',
        'apartment_address',
        'city',
        'state',
        'country',
        'zip',
        'status'
    ]
    list_filter = ['status', 'city', 'state', 'country']
    search_fields = ['user', 'phone_number', 'street_address', 'apartment_address', 'city']


admin.site.register(Address, AddressAdmin)
