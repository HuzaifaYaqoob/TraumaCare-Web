from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem


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
        "order_status",
        "payment_status",
        "created_at",
    ]

    def deliver_at(self, obj):
        return f'{obj.shipping.address}'

    def products(self, obj):
        return ', '.join(obj.order_items.all().values_list('product__name', flat=True))

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
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