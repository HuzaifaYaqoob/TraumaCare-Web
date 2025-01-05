
from django.urls import path, include

from .views import productDetailPage, SingleMedicineViewPage

urlpatterns = [
    path('details/', productDetailPage, name='productDetailPage'),
    path('view/<str:product_slug>/', SingleMedicineViewPage, name='SingleMedicineViewPage'),
]