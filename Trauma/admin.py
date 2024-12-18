from django.contrib import admin

from .models import Speciality, Disease, Country, State, City, RandomFiles, VerificationCode

# Register your models here.
admin.site.site_header = 'Trauma AI Care | Staff Portal'
admin.site.site_title = 'Trauma AI Care | Staff Portal'


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'speciality_type', 'color_code', 'rank' , 'is_deleted', 'is_active']

    search_fields = [ 'name', 'color_code']
    list_editable = ['speciality_type']


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
    list_display = ['id', 'code', 'mobile_number', 'user', 'otp_type', 'is_expired', 'is_deleted', 'is_used']