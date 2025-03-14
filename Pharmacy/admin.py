from django.contrib import admin

# Register your models here.

from .models import Store, StoreLocation, StoreMedia, StoreProductFile



class StoreLocationInline(admin.StackedInline):
    model = StoreLocation
    extra = 0
    exclude = [ 'country', 'state', 'city']

class StoreMediaInline(admin.StackedInline):
    model = StoreMedia
    extra = 0

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = [StoreLocationInline, StoreMediaInline]
    search_fields = ['name']
    list_display = [
        'store', 'locations',
        'created_at', 'updated_at', 'is_active', 'is_blocked',
    ]

    exclude = [ 'profile', 'slug', 'created_at', 'updated_at']
    # 'user',

    @admin.display(description='Store')
    def store(self, obj):
        return obj.store_admin_card()
    store.admin_order_field = 'name'

    def locations(self, store):
        return store.store_locations.count()


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(StoreProductFile)
class StoreProductFileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'store',
        'location',
    ]
