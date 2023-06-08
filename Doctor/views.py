from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from Doctor.models import Doctor


# Create your views here.


def DoctorSearchPage(request):
    return render(request, 'Doctor/doctor_search_page.html')

def DoctorProfilePage(request, doctor_id):
    try:
        doctor = Doctor.objects.get(
            id = doctor_id,
            is_active = True,
            is_deleted = False
        )
    except:
        messages.error(request, 'Invalid Doctor Profile.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        context = {}
        context['doctor'] = doctor
        return render(request, 'Doctor/doctor_view_profile.html', context)