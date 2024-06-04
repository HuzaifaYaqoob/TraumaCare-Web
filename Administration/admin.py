from django.contrib import admin

# Register your models here.

from .models import UserRequestLog

@admin.register(UserRequestLog)
class UserRequestLogAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'real_ip',
        'method',
        'path',
        'user',
        'remote_addr',
        'remote_host',
        'timestamp',
    ]