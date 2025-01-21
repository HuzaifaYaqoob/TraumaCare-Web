from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        "subtotal",
        "discount",
        "platform_fee",
        "delivery_charges",
        "total_amount",
        "payment_method",
        "payment_status",
        "created_at",
    ]