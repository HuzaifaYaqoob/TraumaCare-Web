
from django.urls import path



from .views import homePage, test, emergencyPage, email_view, searchFilterPage, CartPage, FeedPage, SpecialitiesPage, SingleSpecialityPage

urlpatterns = [
    path('', homePage, name='homePage'),
    path('test', test, name='test'),
    path('email/view/', email_view, name='email_view'),
    path('search/', searchFilterPage, name='searchFilterPage'),
    path('cart/', CartPage, name='CartPage'),
    path('feed/', FeedPage, name='FeedPage'),
    path('speciality/', SpecialitiesPage, name='SpecialitiesPage'),
    path('speciality/view/', SingleSpecialityPage, name='SingleSpecialityPage'),
    path('emergency/', emergencyPage, name='emergencyPage'),

] 