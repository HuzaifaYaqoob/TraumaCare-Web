from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem

    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemAdminInline,
    ]
    list_display = [
        'user',
        # "subtotal",
        # "discount",
        # "platform_fee",
        # "delivery_charges",
        "total_amount",
        # "payment_method",
        "payment_status",
        "created_at",
    ]