
from django.urls import path

from django.contrib.auth.decorators import login_required


from .views import homePage, shortCodeRedirect, onboarding, chatXpo_redirection, test, emergencyPage, email_view, searchFilterPage, CartPage, FeedPage, SpecialitiesPage, SingleSpecialityPage, DiseasesViewAllPage, SingleDiseasePage

urlpatterns = [
    path('', homePage, name='homePage'),
    path('st/<str:short_code_id>/', shortCodeRedirect, name='shortCodeRedirect'),
    path('onboarding/', onboarding, name='onboarding'),
    path('chatxpo/', chatXpo_redirection, name='chatXpo_redirection'),
    path('test', test, name='test'),
    path('email/view/', email_view, name='email_view'),
    path('search/', searchFilterPage, name='searchFilterPage'),
    path('cart/', CartPage, name='CartPage'),
    path('feed/', FeedPage, name='FeedPage'),

    path('speciality/', SpecialitiesPage, name='SpecialitiesPage'),
    path('speciality/view/<str:speciality_slug>/', SingleSpecialityPage, name='SingleSpecialityPage'),

    path('diseases/', DiseasesViewAllPage, name='DiseasesViewAllPage'),
    path('diseases/view/<str:disease_slug>/', SingleDiseasePage, name='SingleDiseasePage'),


    path('emergency/', emergencyPage, name='emergencyPage'),

] 