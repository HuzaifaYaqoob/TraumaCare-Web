
from django.urls import path



from .views import homePage, test, searchFilterPage, CartPage, FeedPage

urlpatterns = [
    path('', homePage, name='homePage'),
    path('test', test, name='test'),
    path('search/', searchFilterPage, name='searchFilterPage'),
    path('cart/', CartPage, name='CartPage'),
    path('feed/', FeedPage, name='FeedPage'),

] 