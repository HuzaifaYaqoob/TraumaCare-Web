from django.db import models
from uuid import uuid4
from django.utils.text import slugify

from Authentication.models import User
from Profile.models import Profile
from Trauma.models import Country, State, City
from datetime import timedelta, datetime
from TraumaCare.Constant.index import addWatermark
from django.utils.html import mark_safe



class Store(models.Model): # Medical Store
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name='user_stores')
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, default=None, related_name='profile_stores')
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=999, default='')
    phone = models.CharField(max_length=999, default='')
    email = models.CharField(max_length=999, default='')
    website = models.TextField(default='')

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
 
    def __str__(self):
        return self.store_admin_card()
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(Store, self).save(*args, **kwargs)
    
    @property
    def profile_image(self):
        try:
            profile_pic = StoreMedia.objects.get(
                store = self,
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
    
    def store_admin_card(self, labels=[]):
        div = f"""<div style="display : flex;gap:10px">
                        <span style="width: 50px;height:50px;border:1px solid lightgray;border-radius: 50%;background:url({self.profile_image}) no-repeat center center;background-size:cover"></span>
                        <span>
                            <p style="margin:0;padding:0;font-size:16px">{self.name}</p>
                            <p style="margin:0;padding:0;font-size:13px;font-weight:400;color:black">{self.phone}</p>
                            {f"<span style='margin-top:5px;display:flex;gap:5px;'>{''.join(labels)}</span>" if len(labels) > 0 else ''}
                        </span>
                    </div>"""
        return mark_safe(div)


class StoreLocation(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_locations')
    name = models.CharField(max_length=999, default='')
    address = models.TextField(default='')
    phone = models.CharField(max_length=999, default='')
    email = models.CharField(max_length=999, default='')


    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, default=None, related_name='country_pharmacy_locations')
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, default=None, related_name='state_pharmacy_locations')
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, default=None, related_name='city_pharmacy_locations')

    lat = models.CharField(max_length=999, default='')
    lng = models.CharField(max_length=999, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
 
    def __str__(self):
        return self.name

class StoreMedia(models.Model):


    STORE_MEDIA_TYPES = (
        ('Profile Image', 'Profile Image'),
        ('License', 'License'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_medias')

    file_type = models.CharField(choices=STORE_MEDIA_TYPES, default='Profile Image',max_length=30)
    file = models.FileField(upload_to='PharmacyStore/Files/%Y-%m', help_text='Whenever change Image, You must uncheck "Is Watermark Added"')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_watermark_added = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{str(self.id)} -- '
    
    def save(self, *args, **kwargs):
        if not self.is_watermark_added and self.file and self.file_type == 'Profile Image':
            today_time = datetime.now()
            ext = self.file.name.split('.')[-1]
            self.file = addWatermark(
                self.file, 
                f"media/PharmacyStore/Files/{today_time.year}-{today_time.month}/{self.id}.{ext}"
            )

            self.is_watermark_added = True
        super(StoreMedia, self).save(*args, **kwargs)

