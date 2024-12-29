from django.contrib import admin
from django.db.models import Q

from django.utils.html import mark_safe
from .models import User, Role, StaffRole

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from Profile.models import Profile

COLORS = {
    "Patient" : 'Black',
    "Doctor" : '#0755E9',
    "Hospital" : "#05DC75",
    "Pharmacy" : '#F01275',
    "Lab" : "#F8DB48",
    "Private_Clinic" : '#A737D5',
}

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
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    ordering = ['rank']
    list_display = [
        'name',
        'rank',
        'parent',
        'created_by',
        'status',
        'created_at',
    ]

    exclude = ['slug', 'created_by']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_filter = ['is_active', 'role']
    list_display = [
        'user',
        'roles',
        'is_active',
        'created_at',
    ]

    def roles(self, obj):
        return ', '.join([role.name for role in obj.role.all()])


class UserProfileInline(admin.StackedInline):
    model = Profile
    extra = 0

    exclude = ['email', 'full_name']


class CustomUserAdmin(UserAdmin):
    list_display = [
        'user', 'email', 'first_name', 'last_name', 'joined_at',
        "is_active",
    ]
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'country__name']
    ordering = ['-joined_at']
    list_filter = ['is_admin', 'is_staff', 'is_mobile_verified', 'joined_at']
    inlines = [UserProfileInline]


    # add_fieldsets = (
    #     (
    #         'Create User',
    #         {
    #             "classes": ("wide",),
    #             "fields": (
    #                 # "email",
    #                 "password",
    #                 "username",
    #                 # "first_name",
    #                 # "last_name",
    #             ),
    #         },
    #     ),
    # )
    fieldsets = (
        ("Personal info", {"fields": (
                            "first_name",
                            "last_name",
                            "username",
                            "mobile_number", 
                            "is_mobile_verified", 
                            "email", 
                            "is_email_verified",
                        )}),
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

    def get_label(self, text, color='#0755E9'):
        return f"""<span style="display:inline-block;font-size:11px !important;font-weight:400;padding:2px 5px;border-radius:5px;background-color:{color};color:white">{text}</span>"""
    def user(self, user):
        labels = []
        
        if user.is_superuser:
            labels.append(self.get_label("Superuser", color='#F8DB48'))
        elif user.is_staff or user.is_admin:
            labels.append(self.get_label("Admin Staff", color='#18BFFF'))

        profiles = list(set(user.profiles.values_list('profile_type', flat=True)))
        if 'Patient' in profiles:
            profiles.remove('Patient')

        for p_i, p in enumerate(profiles):
            labels.append(self.get_label(p, COLORS[p]))
        

        is_mobile_verified = '<img style="margin-right:2px" src="%s" />' % ('https://traumaaicare.com/static/admin/img/icon-yes.svg' if user.is_mobile_verified else 'https://traumaaicare.com/static/admin/img/icon-no.svg')
        is_mobile_verified = f'{is_mobile_verified} {user.mobile_number}'
        div = f"""<div style="display : flex;gap:10px">
                    <span style="width: 50px;height:50px;border:1px solid lightgray;border-radius: 50%;background:url({user.profile_image}) no-repeat center center;background-size:cover"></span>
                    <span>
                        <p style="margin:0;padding:0;font-size:16px">{user.full_name}</p>
                        <p style="margin:0;padding:0;font-size:13px;font-weight:400">{is_mobile_verified}</p>
                        <span style='margin-top:5px;display:flex;gap:5px;'>{"".join(labels)}</span>
                    </span>
                </div>"""
        return mark_safe(div)
    
    user.image_tag = True
    user.admin_order_field = "first_name"


    # Methods 
    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        query = Q()
        exclude_query = Q()
        if request.user.is_superuser:
            pass
        elif request.user.is_staff:
            # query &= Q(is_admin=True)
            # query &= Q(is_staff=True)
            exclude_query = Q(is_superuser=True)
        return query_set.filter(query).exclude(exclude_query)

admin.site.register(User, CustomUserAdmin)