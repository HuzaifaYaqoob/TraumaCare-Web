
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from Trauma.views import test, searchFilterPage, CartPage

urlpatterns = [
    path('admin/', admin.site.urls),



    path('application/',  include('Secure.urls')),
    path('api/',  include('Api.urls')),
    path('auth/',  include('Authentication.urls')),
    path('product/',  include('Product.urls')),
    path('doctor/',  include('Doctor.urls')),
    path('blog/',  include('Blog.urls')),
    path('hospital/',  include('Hospital.urls')),
    path('lab/',  include('Lab.urls')),
    path('pharmacy/',  include('Pharmacy.urls')),
    path('appointment/',  include('Appointment.urls')),
    path('medicine/',  include('Medicine.urls')),
    path('cart/',  include('Cart.urls')),
    path('qa/',  include('AskDoctor.urls')),

    path('', include('Trauma.urls')),

] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)