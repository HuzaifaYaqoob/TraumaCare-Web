from django.db import models
from TraumaCare.Constant.index import addWatermark

from uuid import uuid4
from django.utils.html import mark_safe

# Create your models here.
from django.utils.text import slugify

from django.db.models import Q, F

from datetime import datetime, timedelta
from Vendor.models import Vendor
from Pharmacy.models import StoreLocation, Store
from Pharmaceutical.models import Pharmaceutical

# import settings 
from django.conf import settings

import os
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
        new_slug = slugify(f'{self.name} {str(uuid4()).split("-")[0]}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(ProductCategory, self).save(*args, **kwargs)

class SubCategory(models.Model):
    category = models.ManyToManyField(ProductCategory, null=True, related_name='product_category_sub_categories')
    name = models.CharField(max_length=999)
    image = models.ImageField(upload_to='Product/SubCategory/%Y-%m', null=True, blank=True)

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def products(self):
        return Product.objects.filter(sub_category=self)
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {str(uuid4()).split("-")[0]}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(SubCategory, self).save(*args, **kwargs)

class TreatmentType(models.Model):
    name = models.CharField(max_length=999, default='')
    image = models.ImageField(upload_to='Product/TreatmentType/%Y-%m', null=True, blank=True)

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {str(uuid4()).split("-")[0]}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(TreatmentType, self).save(*args, **kwargs)
    

    def products(self):
        return Product.objects.filter(treatment_type=self)


class ProductForm(models.Model):
    name = models.CharField(max_length=999, default='')

    slug = models.CharField(max_length=999, default=uuid4, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = slugify(f'{self.name} {str(uuid4()).split("-")[0]}')
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
        new_slug = slugify(f'{self.name} {str(uuid4()).split("-")[0]}')
        if new_slug != self.slug:
            self.slug = new_slug
        super(ProductType, self).save(*args, **kwargs)


class Product(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')

    Vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=True, related_name='vendor_products')
    manufacturer = models.ForeignKey(Pharmaceutical, on_delete=models.PROTECT, null=True, related_name='manufacturer_products')

    sub_category = models.ManyToManyField(SubCategory, null=True, related_name='sub_category_products')
    treatment_type = models.ForeignKey(TreatmentType, on_delete=models.PROTECT, null=True, related_name='treatment_type_products')
    product_form = models.ForeignKey(ProductForm, on_delete=models.PROTECT, null=True, related_name='product_form_products')
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, null=True, related_name='product_type_products')

    name = models.CharField(max_length=999, default='')
    description = models.TextField(default='')

    price = models.FloatField()
    discount = models.FloatField(default=0, verbose_name='Discount % : ')

    generic_category = models.CharField(max_length=999, default='', null=True, blank=True)
    formulation = models.CharField(max_length=999, default='', null=True, blank=True) # Ingredients
    strength = models.CharField(max_length=999, default='', null=True, blank=True)
    pack_size = models.CharField(max_length=999, default='', null=True, blank=True)
    prescription_required = models.BooleanField(default=False) # True, False
    pack_form = models.CharField(max_length=999, default='', null=True, blank=True)
    key_highlights = models.TextField(default='', null=True, blank=True)
    storage = models.CharField(max_length=999, default='', null=True, blank=True)
    habit_forming  = models.CharField(max_length=999, default='', null=True, blank=True)
    sedation = models.CharField(max_length=999, default='', null=True, blank=True)
    child_safety = models.CharField(max_length=999, default='', null=True, blank=True)
    marketed_by = models.CharField(max_length=999, default='', null=True, blank=True)
    route_of_administration = models.CharField(max_length=999, default='', null=True, blank=True)

    max_order = models.PositiveIntegerField(default=100)

    Images = models.TextField(default='', null=True, blank=True) # To Be Deleted

    sku = models.CharField(max_length=999, default='', null=True, blank=True)
    bar_code = models.CharField(max_length=999, default='', null=True, blank=True)
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
            self.treatment_type.name if self.treatment_type else '',
            self.product_form.name if self.product_form else '',
            self.product_type.name if self.product_type else '',
            str(self.uuid),
        ]
        new_slug = slugify(' '.join(slug_items))
        if new_slug != self.slug:
            self.slug = new_slug
        super(Product, self).save(*args, **kwargs)
    

    @property
    def final_price(self):
        price = self.price
        if self.discount:
            price = self.price - (self.price * self.discount / 100)
        return round(price, 2)
    

    @property
    def discounted_price(self):
        if self.discount:
            price = self.price - (self.price * self.discount / 100)
            return round(price, 2)
        return 0
    
    @property
    def product_all_images(self):
        return self.product_images.all()

    @property
    def cover_image(self):
        try:
            return self.product_images.all()[0].image.url
        except:
            return settings.STATIC_URL + 'assets/Images/medicine-default-img.png'
    
    def product_admin_card(self, labels=[]):
        images = self.product_all_images
        image = images[0].image.url if len(images) > 0 and images[0].image else None
        div = f"""<div style="display : flex;gap:10px">
                        <span style="width: 80px;height:80px;border:1px solid lightgray;border-radius: 50%;background:url({image}) no-repeat center center;background-size:cover"></span>
                        <span style='flex:1'>
                            <p style="margin:0;padding:0;font-size:16px">{self.name}</p>
                            <p style="margin:0;padding:0;font-size:13px;font-weight:400;color:black">{self.store.name} | {self.final_price}</p>
                        </span>
                    </div>"""
        return mark_safe(div)
    
    def lowest_rate_stock(self, location_id=None):
        return self.product_stocks.all()[0]

    def lowest_rate_location(self, location_id=None):
        if not location_id:
            return self.product_stocks.all()[0].location
        for p_st in self.product_stocks.all():
            if p_st.location.id == int(location_id):
                return p_st


class ProductStockCustomManager(models.Manager):
    def get_queryset(self):
        return super(ProductStockCustomManager, self).get_queryset().annotate(
            final_price=F('price') - (F('price') * F('discount') / 100) if F('discount') else F('price')
        )

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

    objects = models.Manager()
    custom_objects = ProductStockCustomManager()

    def __str__(self):
        return f'{self.product.name} - {self.location.name}'

    @property
    def discounted_price(self):
        if self.discount:
            price = self.price - (self.price * self.discount / 100)
            return round(price, 2)
        return round(self.price, 2)
    
    # @property
    # def final_price(self):
    #     price = self.price
    #     if self.discount:
    #         price = self.price - (self.price * self.discount / 100)
    #     return round(price, 2)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_images')
    image = models.ImageField(upload_to='Product/images/%Y-%m/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_watermark_added = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        if not self.is_watermark_added and self.image:
            prev_url = self.image.url
            today_time = datetime.now()
            ext = self.image.name.split('.')[-1]
            if ext not in ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']:
                ext = 'jpg'
            img_slug = slugify(f"{self.product.name} {self.product.treatment_type.name if self.product.treatment_type else ''} traumacare {self.product.store.name}")
            self.image = addWatermark(
                self.image, 
                f"media/Product/images/{today_time.year}-{'0' if today_time.month < 9 else ''}{today_time.month}/{img_slug[:62]}-{today_time.strftime('%d%H%M%S')}.{ext}"
            )

            print(prev_url)
            prev_url = prev_url.replace('/media', 'media')
            # os.remove(prev_url)

            self.is_watermark_added = True
        super(ProductImage, self).save(*args, **kwargs)