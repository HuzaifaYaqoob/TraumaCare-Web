from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from Hospital.models import Hospital
from Doctor.models import Doctor
from django.contrib import messages


def HospitalSearchPage(request):
    return render(request, '')

def ViewHospitalProfile(request, hospital_id):
    try:
        hospital = Hospital.objects.get(id = hospital_id, is_deleted = False, is_active=True, is_blocked = False)
    except:
        messages.error(request, 'Invalid Hospital')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    context = {
        'hospital' : hospital,
    }

    context['doctors'] = Doctor.objects.filter(doctor_hospital_timeslots__hospital = hospital, is_deleted = False, is_blocked = False, is_active = True)

    return render(request, 'Hospital/hospitalprofle.html', context)