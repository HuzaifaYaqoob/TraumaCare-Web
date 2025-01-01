from django.db import models
from uuid import uuid4
from django.utils.text import slugify

class Store(models.Model): # Medical Store
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
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(Store, self).save(*args, **kwargs)


class StoreLocation(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_locations')
    name = models.CharField(max_length=999, default='')
    address = models.TextField(default='')
    phone = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=20, default='')
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



# class Product(models.Model):
#     uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
#     name = models.CharField(max_length=999)
#     description = models.TextField(max_length=999)
#     price = models.FloatField()
#     image = models.ImageField(upload_to='product_images/', null=True, blank=True)

#     sku = models.CharField(max_length=999)
#     bar_code = models.CharField(max_length=999)
    

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_blocked = models.BooleanField(default=False)
 
#     def __str__(self):
#         return self.name