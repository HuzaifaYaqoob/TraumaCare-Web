
from django.urls import path


from . import views as pharmacy_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', pharmacy_views.PharmacyLandingPage, name='PharmacyLandingPage'),
    path('search/', pharmacy_views.PharmacySearchPage, name='PharmacySearchPage'),
    path('cart/', pharmacy_views.PharmacyCartPage, name='PharmacyCartPage'),
    path('cart/checkout/', login_required(pharmacy_views.PharmacyCartCheckoutPage, login_url='/auth/login/'), name='PharmacyCartCheckoutPage'),
] 