
from django.urls import path, include

from . import views, decorators
from .decorators import store_location_url_decorator

urlpatterns = [
    path('upload_store_location_file/', store_location_url_decorator(views.upload_store_location_file) ),
    path('get_store_files/', store_location_url_decorator(views.get_store_files) ),
    path('get_store_file_columns/', store_location_url_decorator(views.get_store_file_columns) ),
    path('save_file_columns/', store_location_url_decorator(views.save_file_columns) ),

    # Image Reading
    path('upload_product_by_image/', store_location_url_decorator(views.upload_product_by_image) ),



    # Location
    path('get_store_locations/', store_location_url_decorator(views.get_store_locations) ),
] 