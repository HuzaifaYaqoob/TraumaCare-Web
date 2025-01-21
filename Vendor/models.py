from django.db import models

# Create your models here.
from django.utils.text import slugify
from uuid import uuid4

from datetime import datetime, timedelta
from TraumaCare.Constant.index import addWatermark

class Vendor(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=999)
    description = models.TextField(max_length=999)

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(Vendor, self).save(*args, **kwargs)

class VendorMedia(models.Model):

    MEDIA_TYPES = (
        ('Profile Image', 'Profile Image'),
        ('License', 'License'),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_media')
    file = models.ImageField(upload_to='Vendor/%Y-%m/')
    file_type = models.CharField(max_length=999, choices=MEDIA_TYPES, default='Profile Image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_watermark_added = models.BooleanField(default=False)
 
    def __str__(self):
        return self.file.name
    

    def save(self, *args, **kwargs):
        if not self.is_watermark_added and self.file and self.file_type == 'Profile Image':
            today_time = datetime.now()
            ext = self.file.name.split('.')[-1]
            self.file = addWatermark(
                self.file, 
                f"media/Vendor/{today_time.year}-{today_time.month}/{self.id}.{ext}"
            )

            self.is_watermark_added = True
        super(VendorMedia, self).save(*args, **kwargs)
