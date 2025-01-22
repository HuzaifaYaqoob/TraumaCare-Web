from django.db import models

from Authentication.models import User
from django.utils.timezone import now
from Product.models import Product, ProductStock
from Profile.models import ShipingAddress
# Create your models here.


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('COD', 'Cash On Delivery'),
        ('ONLINE', 'Online Payment'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELED', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_orders')
    shipping = models.ForeignKey(ShipingAddress, on_delete=models.PROTECT, default=None, related_name='shipping_address_orders')

    subtotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    platform_fee = models.FloatField(default=0)
    delivery_charges = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)

    payment_method = models.CharField(max_length=999, choices=PAYMENT_METHOD_CHOICES, default='COD')
    payment_status = models.CharField(max_length=999, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=now)

    
    def __str__(self):
        return f"{str(self.id)} -- {self.user.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_order_items')
    stock = models.ForeignKey(ProductStock, on_delete=models.PROTECT, related_name='stock_order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    final_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)