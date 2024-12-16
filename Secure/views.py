from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from Secure.models import ApplicationReview
# Create your views here.



def handleApplicationReviewSubmit(request):
    username = request.POST.get('username', 'No Username')
    mobile_number = request.POST.get('mobile_number', 'No Phone')
    star_rating = request.POST.get('star_rating', 1)
    content = request.POST.get('content', 'No Review')

    user = request.user

    ApplicationReview.objects.create(
        user = user if user.is_authenticated else None,
        name = user.full_name if user.is_authenticated else username,
        email = user.email if user.is_authenticated else 'mobile_number@traumaaicare.com',
        phone_number = mobile_number,
        rating = star_rating,
        text = content
    )
    messages.success(request, 'Thanks for reviewing this application')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))