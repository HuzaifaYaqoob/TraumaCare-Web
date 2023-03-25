from django.contrib import admin


from .models import Profile
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'first_name',
        'last_name',
        'full_name',
        'email',
        'profile_type',
        'is_active',
        'is_deleted',
        'is_blocked',
        'created_at',
    ]