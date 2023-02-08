
from django.urls import path, include

from .views import productDetailPage

urlpatterns = [
    path('details/', productDetailPage, name='productDetailPage'),
]