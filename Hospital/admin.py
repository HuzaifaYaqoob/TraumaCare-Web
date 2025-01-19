from django.contrib import admin

# Register your models here.

from .models import *


class HospitalLocationInline(admin.StackedInline):
    model = HospitalLocation
    extra = 1

    fields = [
        # "country",
        "state",
        "city",
        "name",
        "street_address",
        "lat",
        "lng",
    ]


class LocationContactInline(admin.StackedInline):
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
        # 'hospital_and_locations',
        'hospital',
        'doctors',
        'fee',
        'facility_type',
        'website',
        'is_onboard',
        'is_active',
        'is_approved',
    ]

    readonly_fields = ['slug']

    inlines = [
        HospitalLocationInline,
        LocationContactInline,
        HospitalMediaInline,
    ]

    def get_exclude(self, request, obj=None):
        excluded_fields = ['slug', 'fee']
        if obj and obj.pk:
            excluded_fields.extend(['user', 'profile'])
        return excluded_fields

    def hospital_and_locations(self, obj):
        locations = obj.hospital_locations.all()
        return f'{obj.name} ({locations.count()})'
    
    @admin.display(description='Hospital')
    def hospital(self, hospital):
        locations = hospital.hospital_locations.all()
        return hospital.hospital_admin_card(tag_line=f'{locations.count()} Location')
    hospital.admin_order_field = 'name'

    def doctors(self, hospital):
        from Doctor.models import Doctor
        return Doctor.objects.filter(
            doctor_hospital_timeslots__hospital = hospital,
            doctor_hospital_timeslots__is_deleted = False,
            doctor_hospital_timeslots__is_active = True,

            is_active = True,
            is_deleted = False,
            is_blocked = False,
        ).distinct().count()



@admin.register(HospitalLocation)
class HospitalLocationAdmin(admin.ModelAdmin):
    list_filter = [
        'hospital'
    ]
    search_fields = [
        'name',
        'hospital__name',
        'street_address',
        'lat',
        'lng',
    ]
    list_display = [
        'name',
        'hospital',
        'street_address',
        'location',
        'lat',
        'lng',
    ]

    def location(self, location):
        return f'{location.country.name if location.country else "Pakistan"} > {location.state.name if location.state else "---"} > {location.city.name if location.city else "---"}'

@admin.register(LocationContact)
class LocationContactAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'contact_type',
        'contact_title',
        'email',
        'mobile_number',
    ]

@admin.register(HospitalMedia)
class HospitalMediaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'file_type',
    ]

@admin.register(HospitalRequest)
class HospitalRequestAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = [
        'name',
        'phone',
        'is_onboarded',
        'is_active',
        'created_at',
    ]