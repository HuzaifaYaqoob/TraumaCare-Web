from django.contrib import admin
from django.db.models import Q, Count

from django.utils.html import mark_safe
from .models import Doctor, Doctor24By7, DoctorReview, DoctorQuery, DoctorEducation, DoctorExperience, DoctorWithHospital, DoctorDiseasesSpeciality, DoctorMedia, DoctorOnlineAvailability, DoctorSpeciality, DoctorTimeSlots

# Register your models here.


class DoctorDiseasesSpecialityInline(admin.TabularInline):
    model = DoctorDiseasesSpeciality
    extra = 0

class DoctorSpecialityInline(admin.TabularInline):
    model = DoctorSpeciality
    extra = 0

class DoctorMediaInline(admin.TabularInline):
    model = DoctorMedia
    extra = 0   

class DoctorWithHospitalInline(admin.StackedInline):
    model = DoctorWithHospital
    extra = 0   

class DoctorOnlineAvailabilityInline(admin.TabularInline):
    model = DoctorOnlineAvailability
    extra = 0

    fields = ['day', 'is_active', 'is_deleted']

class DoctorTimeSlotsInline(admin.StackedInline):
    model = DoctorTimeSlots
    extra = 0

    exclude = ['discount', 'service_fee']


class Doctor24By7Inline(admin.TabularInline):
    model = Doctor24By7
    extra = 0

class DoctorEducationInline(admin.TabularInline):
    model = DoctorEducation
    extra = 0

class DoctorExperienceInline(admin.TabularInline):
    model = DoctorExperience
    extra = 0

class DoctorReviewInline(admin.TabularInline):
    model = DoctorReview
    extra = 0

class DoctorQueryInline(admin.TabularInline):
    model = DoctorQuery
    extra = 0

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        # 'email', 
        # 'slug', 
        'doctor', 
        # 'mobile_number', 
        'days', 
        'diseases', 
        'speciality', 
        'is_approved', 
        'is_active', 
        'is_deleted', 
        'is_blocked', 
        'is_featured', 
        'is_recommended'
    ]
    search_fields = ['id', 'email', 'name', 'heading', 'mobile_number']

    inlines = [
        DoctorDiseasesSpecialityInline,
        DoctorSpecialityInline,
        DoctorMediaInline,
        DoctorWithHospitalInline,
        DoctorOnlineAvailabilityInline,
        DoctorTimeSlotsInline,
        Doctor24By7Inline,
        DoctorEducationInline,
        DoctorExperienceInline,
        DoctorReviewInline,
        DoctorQueryInline,
    ]

    exclude = [
        'slug',
        'email',
        'online_availability',
        'dial_code',
    ]

    def doctor(self, d):
        return d.doctor_admin_card()

    
    def diseases(self, doctor_instance):
        return DoctorDiseasesSpeciality.objects.filter(
            doctor = doctor_instance
        ).count()
    
    def speciality(self, doctor_instance):
        return DoctorSpeciality.objects.filter(
            doctor = doctor_instance,
            is_deleted = False,
            is_active = True,
        ).count()
    
    def days(self, doctor):
        return DoctorOnlineAvailability.objects.filter(doctor = doctor, is_active = True, is_deleted=False).count()
    days.admin_order_field = 'days'


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(days = Count('doctor_available_days', Where = Q(doctor_available_days__is_active = True, doctor_available_days__is_deleted=False)))



@admin.register(Doctor24By7)
class Doctor24By7Admin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorDiseasesSpeciality)
class DoctorDiseasesSpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'disease']


@admin.register(DoctorMedia)
class DoctorMediaAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorOnlineAvailability)
class DoctorOnlineAvailabilityAdmin(admin.ModelAdmin):
    list_filter = [
        'doctor',
        'day',
        'is_active',
    ]
    search_fields = [
        'doctor__name',
        'day'
    ]
    list_display = [
        'doc',
        'day',
        'is_active',
        'is_deleted',
    ]

    @admin.display(description='Doctor')
    def doc(self, d):
        return d.doctor.doctor_admin_card()
    doc.admin_order_field = 'doctor'


@admin.register(DoctorSpeciality)
class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'speciality']


@admin.register(DoctorTimeSlots)
class DoctorTimeSlotsAdmin(admin.ModelAdmin):
    list_filter = [
        'doctor',
        'doc_hospital__hospital',
    ]
    list_display = [
        'doc',
        'hos',
        'day',
        'title',
        'start_time',
        'end_time',
        'fee',
        'discount',
        # 'service_fee',
        'is_active',
    ]

    @admin.display(description='Doctor')
    def doc(self, d):
        return d.doctor.doctor_admin_card()
    doc.admin_order_field = 'doctor'

    @admin.display(description='Hospital')
    def hos(self, d):
        if d.doc_hospital:
            return d.doc_hospital.hospital.hospital_admin_card(tag_line=d.doc_hospital.location.name)
        return f'{d.availability_type} Slot'
    hos.admin_order_field = 'hospital'


@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorWithHospital)
class DoctorWithHospitalAdmin(admin.ModelAdmin):
    list_filter = [
        'doctor',
        'hospital',
        'is_active',
    ]
    list_display = [
        'doc',
        'hos',
        # 'location',
        'phone',
        'is_active',
    ]
    @admin.display(description='Doctor')
    def doc(self, d):
        return d.doctor.doctor_admin_card()
    doc.admin_order_field = 'doctor'

    @admin.display(description='Hospital')
    def hos(self, d):
        return d.hospital.hospital_admin_card(tag_line=d.location.street_address)
    hos.admin_order_field = 'hospital'

