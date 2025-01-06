from django.db import models
from django.utils.timezone import now

import uuid

from Authentication.models import User


from django.conf import settings
from TraumaCare.Constant.index import addWatermark
from Constants.Data.Profile import DUMMY_PROFILE_IMAGE

import time
from PIL import Image
from datetime import datetime

# Create your models here.


PROFILE_TYPE_LABELS = {
    'Patient' : 'General Profile',
    'Doctor' : 'Doctor Profile',
    'Hospital' : 'Hospital Profile',
    'Pharmacy' : 'Pharmacy Profile',
    'Lab' : 'Lab Profile',
    'Private_Clinic' : 'Private Clinic Profile',
}

class Profile(models.Model):
    PROFILE_CHOICES = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Hospital', 'Hospital'),
        ('Pharmacy', 'Pharmacy'),
        ('Lab', 'Lab'),
        ('Private_Clinic', 'Private_Clinic'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(User, related_name='user_profiles', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=500, default='')
    last_name = models.CharField(max_length=500, default='')
    full_name = models.CharField(max_length=800, default='')
    email = models.EmailField()

    profile_type = models.CharField(default='Patient', choices=PROFILE_CHOICES, max_length=15)
    profile_image = models.ImageField(upload_to='Patients/Images/%Y-%m', default='', help_text='Whenever change Image, You must uncheck "Is Watermark Added"')

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    is_selected = models.BooleanField(default=False)
    is_watermark_added = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.email} - {self.full_name}({self.profile_type}) - - {self.id}'

    @property
    def profile_label(self):
        return PROFILE_TYPE_LABELS.get(self.profile_type, 'General Profile')

    @property
    def huzaifa(self):
        return PROFILE_TYPE_LABELS.get(self.profile_type, 'General Profile')
    
    @property
    def image_full_path(self):
        if self.profile_image:
            return f'{settings.THIS_APPLICATION_URL}{self.profile_image.url}'
        
        return DUMMY_PROFILE_IMAGE
    
    @property
    def mobile_number(self,):
        return self.user.mobile_number

    def save(self, *args, **kwargs):
        if self.profile_type == 'Patient':
            self.first_name = self.user.first_name or self.first_name
            self.last_name = self.user.last_name or self.last_name
            self.email = self.user.email or self.email
        else:
            self.first_name = self.first_name or self.user.first_name
            self.last_name = self.last_name or self.user.last_name
            self.email = self.email or self.user.email
        
        self.full_name = f'{self.first_name} {self.last_name}'.strip()


        if not self.is_watermark_added and self.profile_image:
            today_time = datetime.now()
            ext = self.profile_image.name.split('.')[-1]
            self.profile_image = addWatermark(
                self.profile_image, 
                f"media/Patients/Images/{today_time.year}-{today_time.month}/{self.id}.{ext}"
            )

            self.is_watermark_added = True
        

        super(Profile, self).save(*args, **kwargs)