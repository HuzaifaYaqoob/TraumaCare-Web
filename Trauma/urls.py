
from django.urls import path



from .views import homePage, test, searchFilterPage, CartPage, FeedPage, SpecialitiesPage, SingleSpecialityPage

urlpatterns = [
    path('', homePage, name='homePage'),
    path('test', test, name='test'),
    path('search/', searchFilterPage, name='searchFilterPage'),
    path('cart/', CartPage, name='CartPage'),
    path('feed/', FeedPage, name='FeedPage'),
    path('speciality/', SpecialitiesPage, name='SpecialitiesPage'),
    path('speciality/view/', SingleSpecialityPage, name='SingleSpecialityPage'),

] 