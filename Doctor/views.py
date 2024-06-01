from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from Doctor.models import Doctor, DoctorTimeSlots, DoctorWithHospital, DoctorReview

from Hospital.models import Hospital

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
        context['practicing_locations'] = DoctorWithHospital.objects.filter(doctor = doctor,)
        context['online_availability'] = DoctorTimeSlots.objects.filter(doctor = doctor, availability_type = 'Online', is_deleted = False, is_active=True)
        context['doctor_reviews'] = DoctorReview.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
        context['rating_percentage'] = (sum(context['doctor_reviews'].values_list('rating', flat=True)) / len(context['doctor_reviews'])) / 5 * 100

        return render(request, 'Doctor/doctor_view_profile.html', context)