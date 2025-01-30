
from django.urls import path

from django.contrib.auth.decorators import login_required


from .views import homePage, AboutUsPage, Faqs, CancelationPolicy, TermsOfUsePage, ContactUsPage, PaymentTermsPage, RefundPolicyPage, DeliveryPolicyPage, TermsAndConditions, PrivacyPolicyPage, shortCodeRedirect, onboarding, chatXpo_redirection, test, emergencyPage, email_view, searchFilterPage, CartPage, FeedPage, SpecialitiesPage, SingleSpecialityPage, DiseasesViewAllPage, SingleDiseasePage

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


    path('about-us/', AboutUsPage, name='AboutUsPage'),
    path('contact-us/', ContactUsPage, name='ContactUsPage'),
    path('privacy-policy/', PrivacyPolicyPage, name='PrivacyPolicyPage'),
    path('delivery-policy/', DeliveryPolicyPage, name='DeliveryPolicyPage'),
    path('refund-policy/', RefundPolicyPage, name='RefundPolicyPage'),
    path('payment-terms/', PaymentTermsPage, name='PaymentTermsPage'),
    path('terms-and-conditions/', TermsAndConditions, name='TermsAndConditions'),
    path('terms-of-use/', TermsOfUsePage, name='TermsOfUsePage'),
    path('cancelation-policy/', CancelationPolicy, name='CancelationPolicy'),
    path('faqs/', Faqs, name='Faqs'),

    path('speciality/', SpecialitiesPage, name='SpecialitiesPage'),
    path('speciality/view/<str:speciality_slug>/', SingleSpecialityPage, name='SingleSpecialityPage'),

    path('diseases/', DiseasesViewAllPage, name='DiseasesViewAllPage'),
    path('diseases/view/<str:disease_slug>/', SingleDiseasePage, name='SingleDiseasePage'),


    path('emergency/', emergencyPage, name='emergencyPage'),

] 