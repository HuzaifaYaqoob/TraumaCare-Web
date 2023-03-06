from django.contrib import admin


from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'country_name']

    search_fields = ['id', 'username', 'email', 'country__name']