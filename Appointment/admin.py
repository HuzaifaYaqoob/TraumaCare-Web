from django.contrib import admin

from .models import Appointment, AppointmentGroup
from django.utils.html import mark_safe

# Register your models here.


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'appt',
        'status',
        'doctor_profile',
        "fee",
        'discount',
        'bill',
        'fee_status',
    ]

    raw_id_fields = ['appointment_group', 'doctor', 'slot', 'doct_hospital']

    def appt(self, app):
        return mark_safe(
            f"<div><p style='margin:0;padding:0'>{app.name}</p><p style='margin:0;padding:0;font-size:13px;color:gray;font-weight:500'>{app.date}, {app.start_time} - {app.end_time}</p></div>"
        )

    @admin.display(description='Doctor')
    def doctor_profile(self, app):
        return app.doctor.doctor_admin_card()
    
    list_filter = [
        'date',
        'status',
        'service_fee',
        'fee_status',
        'payment_type',
        'doctor',
    ]

@admin.register(AppointmentGroup)
class AppointmentGroupAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "patient_profile",
        "bill",
        "discount",
        "status",
        "created_at",
    ]