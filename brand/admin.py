from django.contrib import admin
from .models import Brand


class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('user', 'title', 'image_tag', 'is_active', 'created_at')
    search_fields = ['title', 'is_active']
    list_filter = ['title', 'is_active', 'created_at']
    list_editable = ('is_active',)


admin.site.register(Brand, BrandAdmin)
