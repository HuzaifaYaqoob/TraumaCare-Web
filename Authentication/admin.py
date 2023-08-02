from django.contrib import admin


from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['-joined_at']
    list_display = ['id', 'username', 'email', 'country_name', 'joined_at']

    search_fields = ['id', 'username', 'email', 'country__name', 'joined_at']
