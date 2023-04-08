from django.db import models

from django.utils.timezone import now

# Create your models here.

from Authentication.models import User
from Profile.models import Profile
from uuid import uuid4
from Trauma.models import Speciality, Disease
class Doctor(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(User, related_name='doctors', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='profile_doctors', on_delete=models.CASCADE)



    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)


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
