from django.contrib import admin

# Register your models here.

from .models import *


class HospitalLocationInline(admin.TabularInline):
    model = HospitalLocation
    extra = 1

    fields = [
        "name",
        "street_address",
        # "country",
        "state",
        "city",
    ]


class LocationContactInline(admin.TabularInline):
    model = LocationContact
    extra = 2

    fields = [
        "location",
        "contact_type",
        "contact_title",
        "email",
        "mobile_number",
    ]


class HospitalMediaInline(admin.TabularInline):
    model = HospitalMedia
    extra = 1


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]
    list_filter = [
        'facility_type',
        'fee',
        'is_onboard',
        'is_approved',
        'is_active',
        'is_deleted',
        'is_blocked',
        'is_featured',
        'is_recommended',
    ]
    list_display = [
        'hospital_name',
        'fee',
        'facility_type',
        'is_active',
        'is_approved',
    ]

    readonly_fields = ['slug']

    inlines = [
        HospitalLocationInline,
        LocationContactInline,
        HospitalMediaInline,
    ]

    def hospital_name(self, obj):
        locations = obj.hospital_locations.all()
        return f'{obj.name} ({locations.count()})'



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
