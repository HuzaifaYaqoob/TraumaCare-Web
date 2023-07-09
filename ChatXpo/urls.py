
from django.urls import path, include



from .views import Page

urlpatterns = [
    path('xpo/', Page),

] 