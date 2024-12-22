from django.db import models

from django.utils.timezone import now
from uuid import uuid4

from django.utils.html import mark_safe
from TraumaCare.Constant.index import addWatermark


from Authentication.models import User
from Profile.models import Profile
from Trauma.models import Country, State, City
from datetime import timedelta, datetime


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
    website = models.TextField(default='')

    slug = models.TextField(default='')
    fee = models.FloatField(default=0.0, verbose_name='Platform Service Fee(%)')

    is_approved = models.BooleanField(default=False)
    is_onboard = models.BooleanField(default=False)

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
        image = HospitalMedia.objects.filter(
            hospital=self,
            file_type='Profile Image',
            is_deleted=False,
            is_active=True
        ).last()
        if image:
            return image
        return None
    

    @property
    def default_location(self):
        return HospitalLocation.objects.filter(
            hospital=self,
        ).first()


    def __str__(self):
        return f'{str(self.id)} -- {self.name}'

    
    def hospital_admin_card(self, tag_line=None):
        div = f"""<div style="display : flex;gap:10px"><span style="width: 50px;height:50px;border:1px solid lightgray;border-radius: 50%;background:url({self.profile_image.file.url if self.profile_image else "https://ionicframework.com/docs/img/demos/avatar.svg"}) no-repeat center center;background-size:cover"></span><span><p style="margin:0;padding:0;font-size:16px;font-weight:600;color:#007bff">{self.name}</p>{f'<p style="margin:0;padding:0;font-size:13px;font-weight:400;color:black">{tag_line}</p>' if tag_line else ''}</span></div>"""
        return mark_safe(div)
    
    def save(self, *args, **kwargs):
        name = self.name
        name = name.replace(' ', '-').replace('/', '-').replace('--', '-')
        name = name.lower()
        self.slug = f'{name}-{self.uuid}'
        super(Hospital, self).save(*args, **kwargs)


class HospitalLocation(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='hospital_locations')

    name = models.CharField(max_length=999, default='')
    street_address = models.TextField(default='')

    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, default=None, related_name='country_hospital_locations')
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, default=None, related_name='state_hospital_locations')
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, default=None, related_name='city_hospital_locations')

    lat = models.CharField(max_length=999, default='', verbose_name='Latitude')
    lng = models.CharField(max_length=999, default='', verbose_name='Longitude')

    def __str__(self):
        return f'{str(self.id)} -- {self.hospital.name} -- {self.name}'
    
class LocationContact(models.Model):
    CONTACT_TYPE_CHOICES = (
        ('EMAIL', 'EMAIL'),
        ('PHONE_NUMBER', 'PHONE_NUMBER'),
    )
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, related_name='hospital_location_contacts')
    location = models.ForeignKey(HospitalLocation, on_delete=models.PROTECT, related_name='location_contacts')

    contact_type = models.CharField(choices=CONTACT_TYPE_CHOICES, default='EMAIL', max_length=50)
    contact_title = models.CharField(default='', max_length=500)
    email = models.CharField(default='', max_length=500, blank=True)


    dial_code = models.CharField(max_length=20, default='')
    mobile_number = models.CharField(max_length=20, default='', blank=True)

    def __str__(self):
        return f'{str(self.id)} -- {self.hospital.name} -- {self.location.name} -- {self.contact_title}'




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
    file = models.FileField(upload_to='Hospital/Files/%Y-%m', help_text='Whenever change Image, You must uncheck "Is Watermark Added"')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_watermark_added = models.BooleanField(default=False)

    # CNIC Details 
    # cnic_name = models.CharField(max_length=200, default='')
    # cnic_number = models.CharField(max_length=100, default='')
    # cnic_issue_date = models.DateField(null=True)
    # cnic_exp_date = models.DateField(null=True)
    # cnic_dob = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return f'{str(self.id)} -- {self.hospital.name}'
    
    def save(self, *args, **kwargs):
        if not self.is_watermark_added and self.file and self.file_type == 'Profile Image':
            today_time = datetime.now()
            ext = self.file.name.split('.')[-1]
            self.file = addWatermark(
                self.file, 
                f"media/Hospital/Files/{today_time.year}-{today_time.month}/{self.id}.{ext}"
            )

            self.is_watermark_added = True
        super(HospitalMedia, self).save(*args, **kwargs)