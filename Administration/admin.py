from django.contrib import admin

# Register your models here.

from .models import UserRequestLog, PhoneMessage, SmsServiceKey
from Authentication.models import User
from django.utils.html import mark_safe



COLORS = {
    "Patient" : 'Black',
    "Doctor" : '#0755E9',
    "Hospital" : "#05DC75",
    "Pharmacy" : '#F01275',
    "Lab" : "#F8DB48",
    "Private_Clinic" : '#A737D5',
}

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
        'user',
        'sms_type',
        'text',
        'priority',
        'created_at',
        'sms_ids',
        'is_sent',
        'is_deleted',
    ]

    def get_label(self, text, color='#0755E9'):
        return f"""<span style="display:inline-block;font-size:11px !important;font-weight:400;padding:2px 5px;border-radius:5px;background-color:{color};color:white">{text}</span>"""
    def user(self, phone_obj):
        try:
            user_obj = User.objects.get(mobile_number=phone_obj.phone_number)
        except:
            return phone_obj.phone_number

        labels = []
        
        if user_obj.is_superuser:
            labels.append(self.get_label("Superuser", color='#F8DB48'))
        elif user_obj.is_staff or user_obj.is_admin:
            labels.append(self.get_label("Admin Staff", color='#18BFFF'))

        profiles = list(set(user_obj.profiles.values_list('profile_type', flat=True)))
        if 'Patient' in profiles:
            profiles.remove('Patient')

        for p_i, p in enumerate(profiles):
            labels.append(self.get_label(p, COLORS[p]))
        

        is_mobile_verified = '<img style="margin-right:2px" src="%s" />' % ('https://traumaaicare.com/static/admin/img/icon-yes.svg' if user_obj.is_mobile_verified else 'https://traumaaicare.com/static/admin/img/icon-no.svg')
        is_mobile_verified = f'{is_mobile_verified} {user_obj.mobile_number}'
        div = f"""<div style="display : flex;gap:10px">
                    <span style="width: 50px;height:50px;border:1px solid lightgray;border-radius: 50%;background:url({user_obj.profile_image}) no-repeat center center;background-size:cover"></span>
                    <span>
                        <p style="margin:0;padding:0;font-size:16px">{user_obj.full_name}</p>
                        <p style="margin:0;padding:0;font-size:13px;font-weight:400">{is_mobile_verified}</p>
                        <span style='margin-top:5px;display:flex;gap:5px;'>{"".join(labels)}</span>
                    </span>
                </div>"""
        return mark_safe(div)
    
    user.image_tag = True
    user.admin_order_field = "full_name"

@admin.register(SmsServiceKey)
class SmsServiceKeyAdmin(admin.ModelAdmin):
    ordering = ['-updated_at']
    list_display = [
        'id',
        'key',
        'key_provider',
        'updated_at',
    ]