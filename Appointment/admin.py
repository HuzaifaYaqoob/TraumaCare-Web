from django.contrib import admin

from .models import Appointment, AppointmentGroup

# Register your models here.


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'status',
        'date',
        'start_time',
        'end_time',
        "fee",
        'discount',
        'bill',
        'fee_status',
    ]

    list_filter = [
        'date',
        'status',
        'service_fee',
        'fee_status',
        'payment_type',
    ]

@admin.register(AppointmentGroup)
class AppointmentGroupAdmin(admin.ModelAdmin):
    list_display = ['id']