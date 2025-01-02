from django.db import models

from uuid import uuid4
# Create your models here.
from django.utils.text import slugify

from Vendor.models import Vendor
from Pharmacy.models import StoreLocation, Store
from Pharmaceutical.models import Pharmaceutical

# Name 
# Href 
# Categories 
# Vendor
# VendorUrl 
# OriginalPrice
# DiscountedPrice
# CardIngredients (Treatment Type)
# CardPrescriptionRequired
# Generic Category
# Ingredients
# Strength
# Pack Size
# Prescription Required
# Manufacturer
# Country of Origin
# Pack Form
# Product Form
# Product Type
# Key Highlights
# Storage
# Habit Forming
# Sedation
# Child Safety
# Marketed By
# Price
# Sedation
# Route of Administration
# ImagesCount
# Images
# SimilarProducts


class ProductCategory(models.Model):
    name = models.CharField(max_length=999, default='')

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(ProductCategory, self).save(*args, **kwargs)

class SubCategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, related_name='product_category_sub_categories')
    name = models.CharField(max_length=999)

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(SubCategory, self).save(*args, **kwargs)

class TreatmentType(models.Model):
    name = models.CharField(max_length=999, default='')

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(TreatmentType, self).save(*args, **kwargs)


class ProductForm(models.Model):
    name = models.CharField(max_length=999, default='')

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(ProductForm, self).save(*args, **kwargs)

class ProductType(models.Model):
    name = models.CharField(max_length=999, default='')

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {self.uuid}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(ProductType, self).save(*args, **kwargs)


class Product(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')

    Vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=True, related_name='vendor_products')
    manufacturer = models.ForeignKey(Pharmaceutical, on_delete=models.PROTECT, null=True, related_name='manufacturer_products')

    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, null=True, related_name='category_products') 
    sub_category = models.ManyToManyField(SubCategory, null=True, related_name='sub_category_products')
    treatment_type = models.ForeignKey(TreatmentType, on_delete=models.PROTECT, null=True, related_name='treatment_type_products')
    product_form = models.ForeignKey(ProductForm, on_delete=models.PROTECT, null=True, related_name='product_form_products')
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, null=True, related_name='product_type_products')

    name = models.CharField(max_length=999, default='')
    description = models.TextField(default='')
    price = models.FloatField()

    generic_category = models.CharField(max_length=999, default='')
    formulation = models.CharField(max_length=999, default='') # Ingredients
    strength = models.CharField(max_length=999, default='')
    pack_size = models.CharField(max_length=999, default='')
    prescription_required = models.BooleanField(default=False) # True, False
    pack_form = models.CharField(max_length=999, default='')
    key_highlights = models.TextField(default='')
    storage = models.CharField(max_length=999, default='')
    habit_forming  = models.CharField(max_length=999, default='')
    sedation = models.CharField(max_length=999, default='')
    child_safety = models.CharField(max_length=999, default='')
    marketed_by = models.CharField(max_length=999, default='')
    route_of_administration = models.CharField(max_length=999, default='')

    Images = models.TextField(default='') # To Be Deleted

    sku = models.CharField(max_length=999, default='')
    bar_code = models.CharField(max_length=999, default='')
    qr_code = models.ImageField(upload_to='Product/qr_codes/%Y-%m/', null=True, blank=True)
    slug = models.TextField(default=uuid4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
 
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug_items = [
            self.name,
            self.store.name,
            self.Vendor.name if self.Vendor else '',
            self.category.name if self.category else '',
            self.sub_category.name if self.sub_category else '',
            self.treatment_type.name if self.treatment_type else '',
            self.product_form.name if self.product_form else '',
            self.product_type.name if self.product_type else '',
            self.uuid,
        ]
        new_slug = slugify(' '.join(slug_items))
        if new_slug != self.slug:
            self.slug = new_slug
        super(Product, self).save(*args, **kwargs)

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_stocks')
    location = models.ForeignKey(StoreLocation, on_delete=models.PROTECT, related_name='location_stocks')
    quantity = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0, verbose_name='Discount % : ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} - {self.location.name}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_images')
    image = models.ImageField(upload_to='Product/images/%Y-%m/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name