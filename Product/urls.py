
from django.urls import path, include

from .views import productDetailPage, SingleMedicineViewPage, ProductSearchpage

urlpatterns = [
    path('details/', productDetailPage, name='productDetailPage'),
    path('search/', ProductSearchpage, name='ProductSearchpage'),
    path('view/<str:product_slug>/', SingleMedicineViewPage, name='SingleMedicineViewPage'),
]