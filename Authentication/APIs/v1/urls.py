

from django.urls import path, include

from Authentication.APIs.v1 import views as v1_apis
from Authentication.APIs.v1 import custom_admin as admin_apis

urlpatterns = [
    path('validate-unique-user/', v1_apis.vaidate_unique_user, name='vaidate_unique_user' ),

    path('login/', v1_apis.Login ),
    path('signup/', v1_apis.Signup ),

    path('accounts/', include('Authentication.APIs.accounts.urls') ),


    path('admin/get_custom_admin_top_tiles/', admin_apis.getAdminTopTiles, name='getAdminTopTiles' ),
    
] 