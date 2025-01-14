from django.contrib import admin

# Register your models here.

from .models import Pharmaceutical, PharmaceuticalMedia

@admin.register(Pharmaceutical)
class PharmaceuticalAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'products_count']

    def products_count(self, obj):
        return obj.manufacturer_products.count()


@admin.register(PharmaceuticalMedia)
class PharmaceuticalMediaAdmin(admin.ModelAdmin):
    list_display = ['id']