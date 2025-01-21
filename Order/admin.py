from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'shipping',
        # "subtotal",
        # "discount",
        # "platform_fee",
        # "delivery_charges",
        "total_amount",
        # "payment_method",
        "payment_status",
        "created_at",
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "stock",
        "final_price",
        "created_at",
    ]