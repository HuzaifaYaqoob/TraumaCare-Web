
from django.urls import path


from . import views as pharmacy_views

urlpatterns = [
    path('', pharmacy_views.PharmacyLandingPage, name='PharmacyLandingPage'),
    path('search/', pharmacy_views.PharmacySearchPage, name='PharmacySearchPage'),
    path('cart/', pharmacy_views.PharmacyCartPage, name='PharmacyCartPage'),
] 