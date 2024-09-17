from django.contrib import admin

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

    fields = ['day']

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
    list_display = ['id']


@admin.register(DoctorSpeciality)
class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'speciality']


@admin.register(DoctorTimeSlots)
class DoctorTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ['id']

