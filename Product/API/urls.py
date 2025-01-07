
from django.urls import path, include

from .views import CalculateCart

urlpatterns = [
    path('calculate_cart/', CalculateCart, name='CalculateCart'),
]