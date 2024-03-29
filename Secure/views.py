from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from Secure.models import ApplicationReview
# Create your views here.



def handleApplicationReviewSubmit(request):
    username = request.POST.get('username', None)
    user_email = request.POST.get('user_email', None)
    star_rating = request.POST.get('star_rating', None)
    content = request.POST.get('content', None)

    user = request.user

    ApplicationReview.objects.create(
        user = user if user.is_authenticated else None,
        name = user.full_name if user.is_authenticated else username,
        email = user.email if user.is_authenticated else user_email,
        rating = star_rating,
        text = content
    )
    messages.success(request, 'Thanks for reviewing this application')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))