from django.contrib import admin

# Register your models here.

from .models import Vendor, VendorMedia


@admin.register(VendorMedia)
class VendorMediaAdmin(admin.ModelAdmin):
    list_display = ['vendor']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name']