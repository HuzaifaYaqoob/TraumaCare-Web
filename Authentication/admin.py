from django.contrib import admin

from django.utils.html import mark_safe
from .models import User

# Register your models here.

from django.contrib.auth.admin import UserAdmin

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     ordering = ['-joined_at']
#     list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'joined_at']
#     # 'id', 

#     search_fields = ['id', 'username', 'email', 'country__name']
#     list_filter = ['joined_at']

#     def phone_number(self, obj):
#         is_mobile_verified = '<img style="margin-right:7px" src="%s" />' % ('https://traumacare.pk/static/admin/img/icon-yes.svg' if obj.is_mobile_verified else 'https://traumacare.pk/static/admin/img/icon-no.svg')
#         return mark_safe(f'{is_mobile_verified} {obj.mobile_number}')
    
#     phone_number.image_tag = True



class CustomUserAdmin(UserAdmin):
    list_display = ['phone_number', 'username', 'email', 'first_name', 'last_name', 'joined_at']
    search_fields = ['id', 'username', 'email', 'country__name']
    ordering = ['-joined_at']
    list_filter = ['is_mobile_verified', 'joined_at']


    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password",
                    "username",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("mobile_number", "is_mobile_verified", "email", "is_email_verified",)}),
        ("Personal info", {"fields": ("first_name", "last_name", )}),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_staff",
                    "is_blocked",
                    "is_deleted",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    def phone_number(self, obj):
        is_mobile_verified = '<img style="margin-right:7px" src="%s" />' % ('https://traumacare.pk/static/admin/img/icon-yes.svg' if obj.is_mobile_verified else 'https://traumacare.pk/static/admin/img/icon-no.svg')
        return mark_safe(f'{is_mobile_verified} {obj.mobile_number}')
    
    phone_number.image_tag = True
admin.site.register(User, CustomUserAdmin)