



from django.urls import path

from Profile.APIs.v1 import views as api_v1

urlpatterns = [

    path('get-my-sidebar-profiles/', api_v1.get_my_sidebar_profiles),
] 