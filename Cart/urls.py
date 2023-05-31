
from django.urls import path



from .views import CartPage

urlpatterns = [
    path('', CartPage, name='CartPage'),
] 