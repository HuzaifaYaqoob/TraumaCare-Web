from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, ProductCategory, SubCategory, ProductStock, ProductForm, ProductType, TreatmentType
from django.utils.html import mark_safe

from .admin_custom_filters import ImageCountFilter

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = [
        'created_at',
        ImageCountFilter,
    ]
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
        "Images",
    ]
    list_display = [
        'product',
        'price_and_discount',
        'Vendor',
        'manufacturer',
        'formulation',
        'treatment_type',
        'product_form',
        'product_type',
        # 'Images',
    ]


    @admin.display(description='Price & Discount')
    def price_and_discount(self, product):
        return f'{product.price} ({product.discount}%)'

    @admin.display(description='Product')
    def product(self, product):
        return product.product_admin_card()
        
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