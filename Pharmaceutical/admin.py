from django.contrib import admin

# Register your models here.

from .models import Pharmaceutical, PharmaceuticalMedia

@admin.register(Pharmaceutical)
class PharmaceuticalAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(PharmaceuticalMedia)
class PharmaceuticalMediaAdmin(admin.ModelAdmin):
    list_display = ['id']