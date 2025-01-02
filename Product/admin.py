from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, ProductCategory, SubCategory, ProductStock, ProductForm, ProductType, TreatmentType


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product']


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ProductForm)
class ProductFormAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(TreatmentType)
class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name']