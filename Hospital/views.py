from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from Hospital.models import Hospital
from Doctor.models import Doctor
from django.contrib import messages
from Trauma.models import Speciality


def HospitalSearchPage(request):
    return render(request, '')

def ViewHospitalProfile(request, hospital_slug):
    try:
        hospital = Hospital.objects.get(slug = hospital_slug, is_deleted = False, is_active=True, is_blocked = False)
    except:
        messages.error(request, 'Invalid Hospital')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    context = {
        'hospital' : hospital,
    }

    context['doctors'] = Doctor.objects.filter(doctor_hospital_timeslots__hospital = hospital, is_deleted = False, is_blocked = False, is_active = True)
    context['hospital_specialities'] = Speciality.objects.filter(speciality_doctorspecialities__doctor__in = context['doctors']).distinct()

    return render(request, 'Hospital/hospitalprofle.html', context)