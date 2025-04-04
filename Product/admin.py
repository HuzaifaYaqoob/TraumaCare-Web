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
    list_display = ['name', 'products']

    def products(self, obj):
        return obj.products().count()


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline
    ]
    list_filter = [
        'store',
        'Vendor',
        'manufacturer',
        'price',
        'discount',
        'treatment_type',
        ImageCountFilter,
        'created_at',
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
        "description",
        "formulation",
        "strength",
        "pack_form",
        "Images",
    ]
    list_display = [
        'product',
        'categories',
        'price_and_discount',
        'Vendor',
        'manufacturer',
        'formulation',
        'treatment_type',
        'product_form',
        'product_type',
        # 'Images',
    ]

    def categories(self, obj):
        return obj.sub_category.all().count()
    
    categories.admin_order_field = 'sub_category'

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
    list_filter = ['location']
    search_fields = ['product__name', 'location__name']
    list_display = ['product', 'location', 'stock', 'price', 'discount', 'is_active']

    raw_id_fields = ['product', 'location']

    def stock(self, obj):
        return f'{obj.quantity} / {obj.sold}'

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ProductForm)
class ProductFormAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(TreatmentType)
class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'products']
    search_fields = ['name']

    def products(self, obj):
        return obj.products().count()