from django.contrib import admin

from .models import Payment, Order, OrderProduct


def make_refund_accepted(queryset):
    queryset.update(refund_requested=False, refund_granted=True)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('order', 'user', 'product', 'variations', 'quantity', 'ordered', 'created_at')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user',
                    'status', 'being_delivered', 'received', 'refund_requested',
                    'refund_granted', 'shipping_address', 'order_total',
                    'payment', 'created_at']
    list_display_links = [
        'order_number'
    ]
    list_filter = ['user', 'status', 'created_at', 'is_ordered', 'received',
                   'refund_requested', 'refund_granted']
    search_fields = ['order_number', 'user', 'shipping_address',
                     ]
    actions = [make_refund_accepted]
    list_per_page = 20
    inlines = [OrderProductInline]


# class RefundAdmin(admin.ModelAdmin):
#     list_display = ('order', 'reason', 'accepted', 'email')


make_refund_accepted.short_description = 'Update orders to refund granted'
# admin.site.register(Refund, RefundAdmin)
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
