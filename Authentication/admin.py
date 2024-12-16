from django.contrib import admin
from django.db.models import Q

from django.utils.html import mark_safe
from .models import User

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from Profile.models import Profile

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     ordering = ['-joined_at']
#     list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'joined_at']
#     # 'id', 

#     search_fields = ['id', 'username', 'email', 'country__name']
#     list_filter = ['joined_at']

#     def phone_number(self, obj):
#         is_mobile_verified = '<img style="margin-right:7px" src="%s" />' % ('https://traumaaicare.com/static/admin/img/icon-yes.svg' if obj.is_mobile_verified else 'https://traumaaicare.com/static/admin/img/icon-no.svg')
#         return mark_safe(f'{is_mobile_verified} {obj.mobile_number}')
    
#     phone_number.image_tag = True

class UserProfileInline(admin.StackedInline):
    model = Profile
    extra = 0

    exclude = ['email', 'full_name']


class CustomUserAdmin(UserAdmin):
    list_display = ['phone_number', 'username', 'email', 'first_name', 'last_name', 'joined_at']
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'country__name']
    ordering = ['-joined_at']
    list_filter = ['is_admin', 'is_staff', 'is_mobile_verified', 'joined_at']
    inlines = [UserProfileInline]


    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password",
                    "username",
                    # "first_name",
                    # "last_name",
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
    def phone_number(self, user, request):
        is_mobile_verified = '<img style="margin-right:7px" src="%s" />' % ('https://traumaaicare.com/static/admin/img/icon-yes.svg' if user.is_mobile_verified else 'https://traumaaicare.com/static/admin/img/icon-no.svg')
        return mark_safe(f'{is_mobile_verified} {user.mobile_number}')
    
    phone_number.image_tag = True


    # Methods 
    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        query = Q()
        exclude_query = Q()
        if request.user.is_superuser:
            pass
        elif request.user.is_staff:
            query &= Q(is_admin=True)
            query &= Q(is_staff=True)
            exclude_query = Q(is_superuser=True)
        return query_set.filter(query).exclude(exclude_query)

admin.site.register(User, CustomUserAdmin)