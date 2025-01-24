from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem
from django.utils.html import mark_safe
from Constants.global_vars import get_html_label 

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

    readonly_fields = [
        'product',
        'stock',
        'final_price',
        'created_at',
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    inlines = [
        OrderItemInline
    ]
    list_display = [
        'user',
        'deliver_at',
        'products',
        # "subtotal",
        # "discount",
        # "platform_fee",
        # "delivery_charges",
        "total_amount",
        # "payment_method",
        "order_status_labeled",
        "payment_status_labeled",
        "created_at",
    ]

    def deliver_at(self, obj):
        return f'{obj.shipping.address}'

    def products(self, obj):
        return ', '.join(obj.order_items.all().values_list('product__name', flat=True))

    @admin.display(description='Status')
    def order_status_labeled(self, obj):
        color = '#ffb300'
        if obj.order_status == 'SHIPPED':
            color = '#2cccff'
        elif obj.order_status == 'DELIVERED':
            color = '#00e200'
        elif obj.order_status == 'CANCELED':
            color = '#7b808a'
        return mark_safe(get_html_label(obj.order_status, color=color))
    
    @admin.display(description='Payment')
    def payment_status_labeled(self, obj):
        color = '#ffb300'
        if obj.payment_status == 'PAID':
            color = '#00e200' # Green
        elif obj.payment_status == 'CANCELED':
            color = '#7b808a' # Grey
        return mark_safe(get_html_label(obj.payment_status, color=color))
    
    order_status_labeled.admin_order_field = 'order_status'
    payment_status_labeled.admin_order_field = 'payment_status'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    raw_id_fields = [
        'product', 
        'stock'
    ]
    list_filter = [
        'order'
    ]
    list_display = [
        "product",
        "order",
        "stock",
        "final_price",
        "created_at",
    ]