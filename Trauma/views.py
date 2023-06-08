

from django.shortcuts import render, redirect
from django.contrib import messages

from Doctor.models import Doctor
from Trauma.models import Speciality, Disease

def homePage(request):
    context = {}

    doctors = Doctor.objects.all()
    context['doctors'] = doctors
    return render(request, 'Home/index.html', context)

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
        context = {}
        context['speciality'] = speciality
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
    return render(request, 'Disease/SingleDiseaseView.html')

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
    return render(request, 'Emergency/index.html')
