
from django.urls import path, include

from .views import AddProductToCart

urlpatterns = [
    path('add-to-cart/<str:product_slug>/', productDetailPage, name='productDetailPage'),
]