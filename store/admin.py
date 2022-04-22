import admin_thumbnails
from django.contrib import admin

from .models import *


@admin_thumbnails.thumbnail('image')
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'price', 'discount_percentage', 'stock', 'image_tag', 'is_active']
    list_editable = ('is_active',)
    list_filter = ('product', 'color', 'size', 'price', 'discount_percentage', 'is_active')
    search_fields = ['product', 'color', 'size']


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'image_tag']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'updated_at', 'is_available')
    list_editable = ('is_available',)
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        ordering = ['category']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']
    prepopulated_fields = {'slug': ('name',)}


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('type',)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'subject', 'rating')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(SizeType)
admin.site.register(Image, ImagesAdmin)
