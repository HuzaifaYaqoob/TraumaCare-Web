from django.contrib import admin

# Register your models here.

from .models import *


class HospitalLocationInline(admin.TabularInline):
    model = HospitalLocation
    extra = 0

class HospitalMediaInline(admin.TabularInline):
    model = HospitalMedia
    extra = 0

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_filter = [
        'facility_type',
        'is_approved',
        'is_active',
        'is_deleted',
        'is_blocked',
        'is_featured',
        'is_recommended',
    ]
    list_display = [
        'id',
        'name',
        'facility_type',
        'is_approved',
    ]

    inlines = [
        HospitalLocationInline,
        HospitalMediaInline
    ]



@admin.register(HospitalLocation)
class HospitalLocationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'hospital',
        'name',
    ]

@admin.register(LocationContact)
class LocationContactAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'contact_type',
        'contact_title',
        'email',
    ]

@admin.register(HospitalMedia)
class HospitalMediaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file_type',
    ]
