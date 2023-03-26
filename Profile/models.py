from django.db import models
from django.utils.timezone import now

import uuid

from Authentication.models import User

# Create your models here.


class Profile(models.Model):
    PROFILE_CHOICES = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Hospital', 'Hospital'),
        ('Pharmacy', 'Pharmacy'),
        ('Lab', 'Lab'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(User, related_name='user_profiles', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=500, default='')
    last_name = models.CharField(max_length=500, default='')
    full_name = models.CharField(max_length=800, default='')
    email = models.EmailField()

    profile_type = models.CharField(default='Patient', choices=PROFILE_CHOICES, max_length=15)
    profile_image = models.ImageField(upload_to='Patients/Images/%Y-%m', default='')

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.id}'
