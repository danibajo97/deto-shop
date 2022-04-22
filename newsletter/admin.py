from django.contrib import admin

from .models import Subscribe, Contact, Blog


class SubscribeAdmin(admin.ModelAdmin):
    readonly_fields = ('email', 'created_at')


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'title', 'body', 'created_at')


class BlogAdmin(admin.ModelAdmin):
    list_editable = ('is_active',)
    list_display = ['image_tag', 'brand', 'title', 'created_at', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Blog, BlogAdmin)
