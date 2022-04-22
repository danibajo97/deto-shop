from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Account

admin.site.site_header = "Administración de Insomnio"
admin.site.site_title = "Administración de Insomnio"


# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = (
    'image_tag', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active', 'is_seller',
    'is_visitor')
    list_display_links = ('email',)
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
