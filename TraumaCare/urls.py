
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from Trauma.views import homePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePage, name='homePage'),
    path('auth/',  include('Authentication.urls')),

] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)