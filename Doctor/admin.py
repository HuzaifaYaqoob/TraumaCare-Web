from django.contrib import admin

from .models import Doctor, Doctor24By7, DoctorDiseasesSpeciality, DoctorMedia, DoctorOnlineAvailability, DoctorSpeciality, DoctorTimeSlots

# Register your models here.


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'name', 'heading', 'phone_number', 'diseases', 'speciality', 'is_approved', 'is_active', 'is_deleted', 'is_blocked', 'is_featured', 'is_recommended']
    search_fields = ['id', 'email', 'name', 'heading', 'mobile_number']

    
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
    list_display = ['id']


@admin.register(DoctorMedia)
class DoctorMediaAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorOnlineAvailability)
class DoctorOnlineAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorSpeciality)
class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorTimeSlots)
class DoctorTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ['id']

