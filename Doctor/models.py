from django.db import models

from django.utils.timezone import now


# Create your models here.

from Authentication.models import User
from Profile.models import Profile
from uuid import uuid4
from Trauma.models import Speciality, Disease
from Hospital.models import Hospital, HospitalLocation




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

    user = models.ForeignKey(User, related_name='doctors', on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, related_name='profile_doctors', on_delete=models.PROTECT)

    email = models.CharField(max_length=700, default='')
    name = models.CharField(max_length=600, default='')
    heading = models.CharField(max_length=700, default='')

    dial_code = models.CharField(max_length=20, default='')
    mobile_number = models.CharField(max_length=20, default='')

    working_since = models.DateField()

    online_availability = models.CharField(choices=AVAILABILITY_CHOICES, default='24_HOURS_OPEN', max_length=100)

    desc = models.TextField(default='')

    is_approved = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)


    def __str__(self):
        return f'{str(self.id)} -- {self.name}'
    
    @property
    def phone_number(self):
        if self.dial_code and self.mobile_number:
            return f'+{self.dial_code}-{self.mobile_number}'
    
        return ''
    

    @property
    def get_availability_text(self):
        availability = AVAILABILITY_TEXT.get(self.online_availability or '24_HOURS_OPEN')
        return availability
    
    def get_specialities(self,):
        return Speciality.objects.filter(
            speciality_doctorspecialities__doctor = self,
            speciality_doctorspecialities__is_deleted = False,
            speciality_doctorspecialities__is_active = True,
        )
    
    def get_diseases(self,):
        return Disease.objects.filter(
            disease_doctor_disease_specialities__doctor = self,
            disease_doctor_disease_specialities__is_deleted = False,
            disease_doctor_disease_specialities__is_active = True,
        )

    @property
    def specialities(self):
        return self.get_specialities()

    @property
    def diseases(self):
        return self.get_diseases()
    
    @property
    def profile_image(self):
        try:
            profile_pic = DoctorMedia.objects.get(
                doctor = self,
                file_type = 'Profile Image',
                is_deleted = False,
                is_active = True
            )
        except:
            return None
        else:
            if profile_pic.file:
                return profile_pic.file.url
            return None


class DoctorMediaManager(models.Manager):

    def bulk_create(self, objs, **kwargs):
        blk_create = super(models.Manager,self).bulk_create(objs,**kwargs)
        for instance in objs:
            models.signals.post_save.send(instance.__class__, instance=instance, created=True)
        return blk_create
    

class DoctorMedia(models.Model):
    objects = DoctorMediaManager()


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
        return f'{self.speciality.name}'

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
    
    """
        This Table will be used for Doctor Availability with Hospital & Online
    """
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

    class Meta:
        verbose_name = 'Doctor Available Days'

    def __str__(self):
        return f'{self.day} -- Dr. {self.doctor.name}'

class Doctor24By7(models.Model):
    """
        This Table will be used if Doctor is available in case of Emergency. and How much He/She will charge.
        This Model should be OneToOne, Single instance against single Doctor
    """
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_24_availability')

    fee = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    service_fee = models.PositiveIntegerField(default=0, verbose_name='TraumaCare Service FEE in Percentage')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        verbose_name = 'Doctor Availability in Emergency'

    def __str__(self):
        return f'{str(self.id)} -- '


class DoctorTimeSlots(models.Model):
    AVAILABILITY_TYPE = (
        ('Online', 'Online'),
        ('Hospital', 'Hospital'),
    )
    """
        Time Slots Table for Doctor, This Table is for Doctor Online Availability except 24/7,
        This Table also be used for Doctor Availability with Hospital
        ~ If Availability type is Online, It's mean this Object/Record is for Online Availability. Then Hospital Field will be Null
        ~ If Availability type is Hospital, It's mean this Object/Record is for Hospital Availability. Then Hospital Field will be not Null

    """
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_timeslots')
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, null=True, blank=True, related_name='hospital_timeslots')
    location = models.ForeignKey(HospitalLocation, on_delete=models.PROTECT, null=True, blank=True, related_name='location_timeslots')
    day = models.ForeignKey(DoctorOnlineAvailability, on_delete=models.CASCADE, related_name='day_timeslots')

    start_time = models.TimeField()
    end_time = models.TimeField()
    fee = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    service_fee = models.PositiveIntegerField(default=0, verbose_name='TraumaCare Service FEE in Percentage')

    availability_type = models.CharField(choices=AVAILABILITY_TYPE, default='Online', max_length=20)


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        verbose_name = 'Doctor Availability + Fee (Hospital | Online)'


    def __str__(self):
        return f'{str(self.id)} -- '
