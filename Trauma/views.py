

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from Doctor.models import Doctor
from Trauma.models import Speciality, Disease
from django.db.models import Case, When
from rest_framework.authtoken.models import Token
from Secure.models import ApplicationReview

def homePage(request):
    context = {}

    doctors = Doctor.objects.all()
    context['doctors'] = doctors
    context['application_reviews'] = ApplicationReview.objects.filter(is_deleted = False, is_blocked=False).order_by('-rating')[0:20]
    return render(request, 'Home/index.html', context)

def chatXpo_redirection(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login?next=/chatxpo', )

    user_id = request.user.id
    token, created = Token.objects.get_or_create(user = request.user)
    auth_token = token

    accounts_url = f'{settings.ACCOUNT_TRAUMACARE_URL}/auto_login?user_id={user_id}&auth_token={auth_token}'
    reponse = redirect(accounts_url)
    return reponse

def email_view(request):
    path = request.GET.get('path')
    return render(request, path)


def FeedPage(request):
    return render(request, 'Feed/feedPage.html')

def SpecialitiesPage(request):
    return render(request, 'Speciality/specialities.html')

def SingleSpecialityPage(request, speciality_slug):
    
    try:
        speciality = Speciality.objects.get(
            slug = speciality_slug,
            is_deleted = False,
            is_active = True,
        )
    except:
        messages.error(request, 'Invalid Speciality URL!')
        messages.info(request, 'Explore more here!')
        return redirect('SpecialitiesPage')
    else:
        doctor_uri = request.GET.get('doctor_uri', None)
    
        doctors_order_by = []
        if doctor_uri:
            doctors_order_by.append((Case(When(id=doctor_uri, then=0), default=1)))

        context = {}
        context['speciality'] = speciality
        context['doctors'] = Doctor.objects.filter(
            is_active = True,
            is_deleted = False,
            is_blocked = False,
        ).order_by(*doctors_order_by)
        return render(request, 'Speciality/speciality.html', context)


# Diseases Handler 

def DiseasesViewAllPage(request):
    return render(request, 'Disease/Diseases.html')

def SingleDiseasePage(request, disease_slug):
    try:
        disease = Disease.objects.get(
            slug = disease_slug,
            is_deleted = False,
            is_active = True,
        )
    except:
        messages.error(request, 'Invalid disease URL!')
        messages.info(request, 'Explore more here!')
        return redirect('DiseasesViewAllPage')
    else:
        context = {}
        context['disease'] = disease
    return render(request, 'Disease/SingleDiseaseView.html', context)

def test(request):
    return render(request, 'prescription.html')

def CartPage(request):
    return render(request, 'User/cart.html')

def searchFilterPage(request):
    # return render(request, 'Search/booklabtest.html')
    context = {
        'is_search_page' : True,
        'remove_footer' : True
    }
    return render(request, 'Search/Updated_FilterPage.html', context=context)

def emergencyPage(request):
    return render(request, 'Emergency/index.html', {'hide_emergency_icon' : True})
