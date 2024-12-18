from django.contrib import admin


from .models import Profile
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = [
        'full_name',
        'user',
        'email',
        'profile_type',
        'is_active',
        'is_deleted',
        'is_blocked',
        'created_at',
    ]