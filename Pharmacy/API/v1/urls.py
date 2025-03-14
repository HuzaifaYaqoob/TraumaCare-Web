
from django.urls import path, include

from . import views, decorators
from .decorators import store_location_url_decorator

urlpatterns = [
    path('upload_store_location_file/<str:store_id>/<str:location_id>/', views.upload_store_location_file ),
    path('get_store_files/<str:store_id>/<str:location_id>/', store_location_url_decorator(views.get_store_files) ),
    path('get_store_file_columns/<str:store_id>/<str:location_id>/', store_location_url_decorator(views.get_store_file_columns) ),
] 