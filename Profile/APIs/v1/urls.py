



from django.urls import path

from Profile.APIs.v1 import views as api_v1

urlpatterns = [

    path('get-my-sidebar-profiles/', api_v1.get_my_sidebar_profiles),
    path('sidebar-bottom-active-profile/', api_v1.sidebar_bottom_active_profile),
    path('get-dashboard-active-profile-data/', api_v1.get_dashboard_active_profile_data),
    path('switch-my-active-profile/', api_v1.switch_my_active_profile),

    path('get-already-registered-profiles/', api_v1.get_already_registered_businesses),

] 