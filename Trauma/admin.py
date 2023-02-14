from django.contrib import admin

from .models import Speciality

# Register your models here.



@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color_code', 'rank' , 'is_deleted', 'is_active']

    search_fields = [ 'name', 'color_code']