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
    search_fields = [
        'name', 
        "store__name",
        "Vendor__name",
        "manufacturer__name",
        "treatment_type__name",
        "product_form__name",
        "product_type__name",
        "generic_category",
        "formulation",
        "strength",
        "pack_form",
    ]
    list_display = [
        'name',
        'price',
        'discount',
        'product_store',
        'Vendor',
        'manufacturer',
        'formulation',
        'treatment_type',
        'product_form',
        'product_type',
        'product_image',
        'Images',
    ]

    @admin.display(description='Store')
    def product_store(self, obj):
        return obj.store
    product_store.admin_order_field = 'store'

    @admin.display(description='Images')
    def product_image(self, product):
        imgs = ProductImage.objects.filter(product=product)
        return mark_safe(f"""<div class='d-flex' >{''.join([f'<img loading="lazy" src="{img.image.url if img.image else None}" alt="{product.name}" style="max-width:100px;max-height:100px;" />' for img in imgs])}</div>""")
        
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'product_image']

    @admin.display(description='Image')
    def product_image(self, img):
        return mark_safe(f"""<img loading="lazy" src="{img.image.url if img.image else None}" alt="{img.product.name}" style="max-width:100px;max-height:100px;" />""")
        


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