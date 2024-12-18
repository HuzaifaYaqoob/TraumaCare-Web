
from django.urls import path


from . import views as business_views

urlpatterns = [
    path('search/', business_views.BusinessSearchPage, name='BusinessSearchPage')
] 