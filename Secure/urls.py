
from django.urls import path

from . import views as secure_views

urlpatterns = [
    path('submit-application-review/', secure_views.handleApplicationReviewSubmit, name='handleApplicationReviewSubmit')
] 