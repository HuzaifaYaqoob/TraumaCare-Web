from django.contrib import admin


from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['-joined_at']
    list_display = ['username', 'email', 'first_name', 'last_name', 'mobile_number', 'is_mobile_verified', 'joined_at']
    # 'id', 

    search_fields = ['id', 'username', 'email', 'country__name']
    list_filter = ['joined_at']
