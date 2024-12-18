
from django.urls import path


from . import views as pharmacy_views

urlpatterns = [
    path('search/', pharmacy_views.PharmacySearchPage, name='PharmacySearchPage')
] 