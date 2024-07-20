from django.db import models

# Create your models here.

import uuid
from Authentication.models import User


class UserRequestLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user_logs')

    log_requests = models.PositiveIntegerField(default=0)

    country = models.CharField(max_length=999, null=True, blank=True)
    city = models.CharField(max_length=999, null=True, blank=True)
    country_code = models.CharField(max_length=999, null=True, blank=True)
    lat = models.CharField(max_length=999, null=True, blank=True)
    lng = models.CharField(max_length=999, null=True, blank=True)
    postal_code = models.CharField(max_length=999, null=True, blank=True)
    geo_data = models.TextField(null=True, blank=True)

    method = models.CharField(max_length=100, default='')
    path = models.CharField(max_length=500)
    real_ip = models.CharField(max_length=999, blank=True, null=True)


    timestamp = models.DateTimeField(auto_now_add=True)
    response_status = models.IntegerField()
    data = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.real_ip} - {self.path} at {self.timestamp}"
    


class PhoneMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.TextField()
    text = models.TextField()
    mask = models.CharField(max_length=999, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sent = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.phone_number
    
    def save(self, *args, **kwargs):
        if not self.mask:
            self.mask = 'REDEXPO'
        super(PhoneMessage, self).save(*args, **kwargs)