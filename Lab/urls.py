
from django.urls import path


from . import views as lab_views

urlpatterns = [
    path('search/', lab_views.LabSearchPage, name='LabSearchPage')
] 