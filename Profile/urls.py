
from django.urls import path

from . import views as profile_views

urlpatterns = [
    path('test/', profile_views.test, name='test')
] 