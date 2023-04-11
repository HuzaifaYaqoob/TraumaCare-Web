from django.db import models

from django.utils.timezone import now

# Create your models here.

from Authentication.models import User
from Profile.models import Profile
from uuid import uuid4
from Trauma.models import Speciality, Disease




AVAILABILITY_TEXT = {
    '24_HOURS_OPEN' : '24 Hours Open',
    'AVAILABILITY_TIME_SLOTS' : 'Available on Timeslots',
}

class Doctor(models.Model):

    AVAILABILITY_CHOICES = (
        ('24_HOURS_OPEN', '24_HOURS_OPEN'),
        ('AVAILABILITY_TIME_SLOTS', 'AVAILABILITY_TIME_SLOTS'),
    )


    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(User, related_name='doctors', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='profile_doctors', on_delete=models.CASCADE)

    email = models.CharField(max_length=700, default='')
    name = models.CharField(max_length=600, default='')
    heading = models.CharField(max_length=700, default='')

    dial_code = models.CharField(max_length=20, default='')
    mobile_number = models.CharField(max_length=20, default='')

    working_since = models.DateField()

    online_availability = models.CharField(choices=AVAILABILITY_CHOICES, default='24_HOURS_OPEN', max_length=100)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- '
    

    @property
    def get_availability_text(self):
        availability = AVAILABILITY_TEXT.get(self.online_availability or '24_HOURS_OPEN')
        return availability


class DoctorMedia(models.Model):
    DOCTOR_MEDIA_TYPES = (
        ('Profile Image', 'Profile Image'),
        ('CNIC Front', 'CNIC Front'),
        ('CNIC Back', 'CNIC Back'),
        ('License', 'License'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_medias')

    file_type = models.CharField(choices=DOCTOR_MEDIA_TYPES, default='Profile Image',max_length=30)
    file = models.FileField(upload_to='Doctor/Files/%Y-%m')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- '


class DoctorSpeciality(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_specialities')
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, related_name='speciality_doctorspecialities')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- '

class DoctorDiseasesSpeciality(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_disease_specialities')
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, related_name='disease_doctor_disease_specialities')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- '


class DoctorOnlineAvailability(models.Model):
    DAYS_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_available_days')


    day = models.CharField(choices=DAYS_CHOICES, default='Monday', max_length=20)


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)



    def __str__(self):
        return f'{str(self.id)} -- '

class DoctorTimeSlots(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_timeslots')
    day = models.ForeignKey(DoctorOnlineAvailability, on_delete=models.CASCADE, related_name='day_timeslots')

    start_time = models.TimeField()
    end_time = models.TimeField()
    fee = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    service_fee = models.PositiveIntegerField(default=0, verbose_name='TraumaCare Service FEE in Percentage')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- '
