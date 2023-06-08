

from django.shortcuts import render

from Doctor.models import Doctor
from Trauma.models import Speciality

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
    specialities = Speciality.objects.all()
    return render(request, 'Speciality/specialities.html' , context={'all_specialities' : specialities})

def SingleSpecialityPage(request):
    return render(request, 'Speciality/speciality.html')

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
