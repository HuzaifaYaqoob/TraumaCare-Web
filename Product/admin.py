from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, ProductCategory, SubCategory, ProductStock, ProductForm, ProductType, TreatmentType
from django.utils.html import mark_safe


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        'name',
        'price',
        'product_store',
        'Vendor',
        'manufacturer',
        'treatment_type',
        'product_form',
        'product_type',
        'Images',
    ]

    @admin.display(description='Store')
    def product_store(self, obj):
        return obj.store
    product_store.admin_order_field = 'store'

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