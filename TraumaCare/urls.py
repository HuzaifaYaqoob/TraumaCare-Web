
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from Trauma.views import homePage, test, searchFilterPage, CartPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePage, name='homePage'),
    path('test', test, name='test'),
    path('search/', searchFilterPage, name='searchFilterPage'),
    path('cart/', CartPage, name='CartPage'),



    path('auth/',  include('Authentication.urls')),
    path('product/',  include('Product.urls')),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)