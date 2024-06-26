from django.contrib import admin

from django.utils.html import mark_safe
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['-joined_at']
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_mobile_verified', 'joined_at']
    # 'id', 

    search_fields = ['id', 'username', 'email', 'country__name']
    list_filter = ['joined_at']

    def phone_number(self, obj):
        is_mobile_verified = '<img src="https://traumacare.pk/static/admin/img/icon-yes.svg" />' if obj.is_mobile_verified else '<img src="https://traumacare.pk/static/admin/img/icon-no.svg" />'
        return mark_safe(f'{is_mobile_verified} {obj.mobile_number}')
    
    phone_number.image_tag = True
