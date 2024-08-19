from django.contrib import admin

# Register your models here.

from .models import UserRequestLog, PhoneMessage, SmsServiceKey

@admin.register(UserRequestLog)
class UserRequestLogAdmin(admin.ModelAdmin):

    list_filter = [
        'real_ip',
        'response_status',
        'user',
        'method',
    ]

    list_display = [
        'id',
        'real_ip',
        'location',
        'log_requests',
        'response',
        'path',
        'user',
        'timestamp',
    ]


    def location(self, log):
        return f'{log.city}, {log.country} ({log.country_code})'
    
    def response(self, log):
        return f'{log.method} {log.response_status}'


@admin.register(PhoneMessage)
class PhoneMessageAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
    list_display = [
        'phone_number',
        'sms_type',
        'text',
        'priority',
        'created_at',
        'sms_ids',
        'is_sent',
        'is_deleted',
    ]

@admin.register(SmsServiceKey)
class SmsServiceKeyAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
    list_display = [
        'id',
        'key',
        'key_provider',
        'updated_at',
    ]