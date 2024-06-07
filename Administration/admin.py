from django.contrib import admin

# Register your models here.

from .models import UserRequestLog

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
        'log_requests',
        'method',
        'path',
        'user',
        'timestamp',
        'response_status',
        'query_params',
    ]