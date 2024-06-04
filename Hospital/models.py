from django.db import models

from django.utils.timezone import now
from uuid import uuid4

from Authentication.models import User
from Profile.models import Profile


class Hospital(models.Model):
    FACILITY_TYPE_CHOICES = (
        ('Hospital', 'Hospital'),
        ('Private_Clinic', 'Private Clinic')
    )
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

    user = models.ForeignKey(User, related_name='hospitals', on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, related_name='profile_hospitals', on_delete=models.PROTECT)

    facility_type = models.CharField(max_length=50, default='Hospital', choices=FACILITY_TYPE_CHOICES)
    name = models.CharField(max_length=777, default='')
    description = models.TextField(default='')

    slug = models.TextField(default='')

    is_approved = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)

    class Meta:
        verbose_name = 'HealthCare Facility, Hospital or Private Clinic'
    
    @property
    def profile_image(self):
        return HospitalMedia.objects.filter(
            hospital=self,
            file_type='Profile Image',
            is_deleted=False,
            is_active=True
        ).last()


    def __str__(self):
        return f'{str(self.id)} -- {self.name}'
    
    def save(self, *args, **kwargs):
        name = self.name
        name = name.replace(' ', '-').replace('/', '-').replace('--', '-')
        name = name.lower()
        self.slug = f'{name}-{self.uuid}'
        super(Hospital, self).save(*args, **kwargs)


class HospitalLocation(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

    user = models.ForeignKey(User, related_name='hospital_locations', on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, related_name='profile_hospital_locations', on_delete=models.PROTECT)

    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='hospital_locations')

    name = models.CharField(max_length=999, default='')
    street_address = models.TextField(default='')

    def __str__(self):
        return f'{str(self.id)} -- {self.hospital.name} -- {self.name}'

class LocationContact(models.Model):
    CONTACT_TYPE_CHOICES = (
        ('EMAIL', 'EMAIL'),
        ('PHONE_NUMBER', 'PHONE_NUMBER'),
    )
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, related_name='hospital_location_contacts', on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, related_name='profile_hospital_location_contacts', on_delete=models.PROTECT)

    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='hospital_location_contacts')
    location = models.ForeignKey(HospitalLocation, on_delete=models.PROTECT, related_name='location_contacts')

    contact_type = models.CharField(choices=CONTACT_TYPE_CHOICES, default='EMAIL', max_length=50)
    contact_title = models.CharField(default='', max_length=500)
    email = models.CharField(default='', max_length=500)


    dial_code = models.CharField(max_length=20, default='')
    mobile_number = models.CharField(max_length=20, default='')

    def __str__(self):
        return f'{str(self.id)} -- {self.hospital.name} -- {self.location.name} -- {self.contact_title}'

    @property
    def phone_number(self):
        if self.dial_code and self.mobile_number:
            return f'+{self.dial_code}-{self.mobile_number}'
    
        return ''



class HospitalMediaManager(models.Manager):

    def bulk_create(self, objs, **kwargs):
        blk_create = super(models.Manager,self).bulk_create(objs,**kwargs)
        for instance in objs:
            models.signals.post_save.send(instance.__class__, instance=instance, created=True)
        return blk_create

class HospitalMedia(models.Model):
    objects = HospitalMediaManager()

    HOSPITAL_MEDIA_TYPES = (
        ('Profile Image', 'Profile Image'),
        ('CNIC Front', 'CNIC Front'),
        ('CNIC Back', 'CNIC Back'),
        ('License', 'License'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='hospital_medias')

    file_type = models.CharField(choices=HOSPITAL_MEDIA_TYPES, default='Profile Image',max_length=30)
    file = models.FileField(upload_to='Hospital/Files/%Y-%m')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # CNIC Details 
    # cnic_name = models.CharField(max_length=200, default='')
    # cnic_number = models.CharField(max_length=100, default='')
    # cnic_issue_date = models.DateField(null=True)
    # cnic_exp_date = models.DateField(null=True)
    # cnic_dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return f'{str(self.id)} -- {self.hospital.name}'