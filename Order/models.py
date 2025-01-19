from django.db import models

from Authentication.models import User
from django.utils.timezone import now
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_orders')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=now)