
from django.urls import path


from . import views as medicine_views

urlpatterns = [
    path('', medicine_views.AllMedicinesPage, name='AllMedicinesPage'),
    path('view/<str:id>/', medicine_views.SingleMedicineViewPage, name='SingleMedicineViewPage'),
] 