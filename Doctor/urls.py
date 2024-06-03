
from django.urls import path


from . import views as doctor_views


urlpatterns = [
    path('search/', doctor_views.DoctorSearchPage, name='DoctorSearchPage'),
    path('profile/view/<str:doctor_id>/', doctor_views.DoctorProfilePage, name='DoctorProfilePage'),
    path('profile/view/<str:doctor_id>/ask-question', doctor_views.DoctorAskQuestionHandler, name='DoctorAskQuestionHandler'),
] 