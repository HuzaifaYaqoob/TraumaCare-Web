
from django.urls import path


from . import views 


urlpatterns = [
    path('', views.BlogHomePage, name='BlogHomePage'),
    path('<str:post_slug>/', views.PostViewPage, name='PostViewPage'),
] 