
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from Trauma.views import test, searchFilterPage, CartPage
from .views import set_language
from .admin_views import OrganizationHierarchyPage, SuperUserDashboard, AdminTestPage

from Administration import views as administration_views

import debug_toolbar

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/organization/', OrganizationHierarchyPage, name='OrganizationHierarchyPage'),
    path('admin/super-dashboard/', SuperUserDashboard, name='SuperUserDashboard'),
    path('admin/test/', AdminTestPage, name='AdminTestPage'),
    path('admin/', admin.site.urls),



    path('set_language/',  set_language, name='set_language'),
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

handler500 = 'Trauma.views.Custom500ErrorPage'
handler403 = 'Trauma.views.Custom400ErrorPage'
handler404 = 'Trauma.views.Custom400ErrorPage'
handler400 = 'Trauma.views.Custom400ErrorPage'


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)