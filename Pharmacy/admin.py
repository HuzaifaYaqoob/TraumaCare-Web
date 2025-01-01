from django.contrib import admin

# Register your models here.

from .models import Store, StoreLocation, StoreMedia



class StoreLocationInline(admin.TabularInline):
    model = StoreLocation
    extra = 0

class StoreMediaInline(admin.TabularInline):
    model = StoreMedia
    extra = 0

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = [StoreLocationInline, StoreMediaInline]
    list_display = [
        'name', 'phone',
        'created_at', 'updated_at', 'is_active', 'is_blocked',
    ]