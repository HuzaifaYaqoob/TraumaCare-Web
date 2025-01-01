from django.db import models

# Create your models here.
from django.utils.text import slugify


# class ProductCategory(models.Model):
#     uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
#     name = models.CharField(max_length=999)
#     description = models.TextField(max_length=999)

#     slug = models.CharField(max_length=999, default=uuid4, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
 
#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         new_slug = slugify(f'{self.name} {self.uuid}')
#         if new_slug != self.slug:
#             self.slug = new_slug
#         super(ProductCategory, self).save(*args, **kwargs)

# class ProductSubCategory(models.Model):
#     uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
#     category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='product_category_sub_categories')
#     name = models.CharField(max_length=999)
#     description = models.TextField(max_length=999)

#     slug = models.CharField(max_length=999, default=uuid4, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
 
#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         new_slug = slugify(f'{self.name} {self.uuid}')
#         if new_slug != self.slug:
#             self.slug = new_slug
#         super(ProductSubCategory, self).save(*args, **kwargs)

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