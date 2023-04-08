



from django.urls import path, include

urlpatterns = [

    path('', include('Trauma.APIs.v1.urls') ),
] 