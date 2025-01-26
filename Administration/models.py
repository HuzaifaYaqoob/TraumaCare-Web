from django.db import models

# Create your models here.

import uuid
from Authentication.models import User
import re

def convert_phone_number(phone_number):
    pattern = r'^(?:\+92|92|0)?(\d{10})$'
    replacement = r'92\1'
    return re.sub(pattern, replacement, phone_number)

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


class SmsServiceKey(models.Model):
    KEY_PROVIDER_CHOICES = (
        ('Telenor', 'Telenor'),
        ('Jazz', 'Jazz'),
        ('Zong', 'Zong'),
    )

    key = models.TextField()
    key_provider = models.CharField(max_length=999, default='Telenor', choices=KEY_PROVIDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.key


class PhoneMessage(models.Model):
    SMS_TYPE_CHOICES = (
        ('OTP', 'OTP'),
        ('Appointment', 'Appointment'),
        ('OnlineAppointment', 'OnlineAppointment'),
        ('DoctorWithHospital', 'DoctorWithHospital'),
        ('ExpiredAppointment', 'ExpiredAppointment'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.TextField()
    text = models.TextField()
    mask = models.CharField(max_length=999, null=True, blank=True)
    sms_type = models.CharField(max_length=999, null=True, blank=True, choices=SMS_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sent = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    sms_ids = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    priority = models.IntegerField(default=10)


    def __str__(self):
        return self.phone_number
    
    def save(self, *args, **kwargs):
        if self.phone_number == '0000':
            self.is_deleted = True
            
        if self.sms_type == 'OTP':
            self.priority = 1
        elif self.sms_type == 'Appointment' or self.sms_type == 'OnlineAppointment':
            self.priority = 2

        if not self.mask:
            self.mask = 'REDEXPO'
        super(PhoneMessage, self).save(*args, **kwargs)


class SiteSetting(models.Model):
    pharmacy_platform_fee = models.FloatField(default=0)
    appointment_platform_fee = models.FloatField(default=0)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmailLog(models.Model):
    emails = models.CharField(max_length=999, default='')
    subject = models.CharField(max_length=999, default='')
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    error = models.TextField(null=True, blank=True)

class PageAnalytics(models.Model):
    ANALYTIC_TYPE_CHOICES = (
        ('Views', 'Views'),
        ('Clicks', 'Clicks'),
        ('Visits', 'Visits'),
    )
    value = models.PositiveIntegerField(default=0)
    urls = models.TextField()
    analytic_type = models.CharField(max_length=999, choices=ANALYTIC_TYPE_CHOICES, default='Views')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)