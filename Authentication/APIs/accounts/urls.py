

from django.urls import path

from Authentication.APIs.accounts import views as accounts_views

urlpatterns = [
    path('get_user_profiles_data/', accounts_views.getUserProfilesData ),

] 