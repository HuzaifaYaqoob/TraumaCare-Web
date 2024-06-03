from django.contrib import admin

from .models import Appointment, AppointmentGroup

# Register your models here.


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(AppointmentGroup)
class AppointmentGroupAdmin(admin.ModelAdmin):
    list_display = ['id']