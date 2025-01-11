from django.contrib import admin

from .models import Speciality, Disease, Country, State, City, RandomFiles, VerificationCode
from django.utils.html import mark_safe


# Register your models here.
admin.site.site_header = 'Trauma AI Care | Staff Portal'
admin.site.site_title = 'Trauma AI Care | Staff Portal'


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['speciality_with_icon', 'doctors', 'speciality_type', 'color_code', 'rank' , 'is_deleted', 'is_active']

    search_fields = [ 'name', 'color_code']
    list_editable = ['speciality_type']

    def doctors(self, speciality):
        return speciality.speciality_doctorspecialities.count()
    doctors.admin_order_field = 'speciality_doctorspecialities'
    
    @admin.display(description='Speciality')
    def speciality_with_icon(self, speciality):
        return mark_safe(f'<span>{speciality.svg_icon}<span> {speciality.name}</span></span>')
    speciality_with_icon.admin_order_field = 'name'
    


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'speciality', 'color_code', 'rank', 'is_description' , 'is_deleted', 'is_active']

    search_fields = [ 'name', 'color_code', 'speciality']
    list_filter = ['speciality']

    def is_description(self, disease_intance):
        if disease_intance.description:
            return True
        
        return False

    is_description.boolean = True


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color_code', 'is_deleted', 'is_active']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color_code', 'is_deleted', 'is_active']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color_code', 'is_deleted', 'is_active']

@admin.register(RandomFiles)
class RandomFilesAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    search_fields = ['mobile_number']
    list_display = ['user_', 'mobile_number','code', 'otp_type', 'is_expired', 'is_deleted', 'is_used', 'created_at']


    @admin.display(description='User')
    def user_(self, v_obj):
        user = v_obj.user
        is_mobile_verified = '<img style="margin-right:2px" src="%s" />' % ('https://traumaaicare.com/static/admin/img/icon-yes.svg' if user.is_mobile_verified else 'https://traumaaicare.com/static/admin/img/icon-no.svg')
        is_mobile_verified = f'{is_mobile_verified} {user.mobile_number}'
        div = f"""<div style="display : flex;gap:10px">
                    <span style="width: 50px;height:50px;border:1px solid lightgray;border-radius: 50%;background:url({user.profile_image}) no-repeat center center;background-size:cover"></span>
                    <span>
                        <p style="margin:0;padding:0;font-size:16px">{user.full_name}</p>
                        <p style="margin:0;padding:0;font-size:13px;font-weight:400">{is_mobile_verified}</p>
                    </span>
                </div>"""
        return mark_safe(div)
    
    user_.image_tag = True
    user_.admin_order_field = "first_name"