from django.db import models


from uuid import uuid4
from Doctor.models import Doctor, DoctorWithHospital, DoctorTimeSlots
from Authentication.models import User
from Hospital.models import Hospital, HospitalLocation
from datetime import datetime
# Create your models here.


class AppointmentGroup(models.Model):
    APPOINTMENT_STATUSES = (
        ('Booked', 'Booked'),
        ('Finished', 'Finished'),
        ('Cancelled', 'Cancelled'),
    )
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_appointments')

    bill = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=999, choices=APPOINTMENT_STATUSES, default='Booked')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Appointment(models.Model):
    APPOINTMENT_STATUSES = (
        ('Pending', 'Pending'),
        ('Booked', 'Booked'),
        ('Confirmed', 'Confirmed'),
        ('Finished', 'Finished'),
        ('Cancelled', 'Cancelled'),
    )

    APPOINTMENT_LOCATION_CHOICES = (
        ('Online', 'Online'),
        ('InPerson', 'InPerson'),
    )

    PAYMENT_STATUS = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )

    PAYMENT_TYPE = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
    )

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    appointment_group = models.ForeignKey(AppointmentGroup, on_delete=models.CASCADE, related_name='appointments')

    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='doctor_appointments')

    name = models.CharField(default='', max_length=999)
    instructions = models.TextField(default='', null=True, blank=True)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    slot = models.ForeignKey(DoctorTimeSlots, on_delete=models.PROTECT, null=True, blank=True, related_name='slot_appointments')

    fee = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    service_fee = models.PositiveIntegerField(default=0)
    bill = models.PositiveIntegerField(default=0)
    fee_status = models.CharField(max_length=999, choices=PAYMENT_STATUS, default='Unpaid')
    payment_type = models.CharField(max_length=999, choices=PAYMENT_TYPE, default='Cash')

    status = models.CharField(max_length=999, choices=APPOINTMENT_STATUSES, default='Pending')
    appointment_location = models.CharField(max_length=999, choices=APPOINTMENT_LOCATION_CHOICES, default='InPerson')

    doct_hospital = models.ForeignKey(DoctorWithHospital, on_delete=models.PROTECT, null=True, blank=True, related_name='doct_hospital_appointments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def day_name(self):
        if self.date:
            # Short Day name
            return self.date.strftime('%a')
        
        return None

    @property
    def user(self):
        return self.appointment_group.user
    
    @property
    def is_today(self):
        if self.date:
            return datetime.now().date() == self.date
        
    @property
    def date_prefix_zero(self):
        if self.date:
            return self.date.strftime('%d')
        
    def __str__(self):
        return str(self.id)