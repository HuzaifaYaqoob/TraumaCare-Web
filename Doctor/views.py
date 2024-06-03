from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from Doctor.models import Doctor, DoctorTimeSlots, DoctorWithHospital, DoctorReview, DoctorEducation, DoctorExperience, DoctorQuery

from Hospital.models import Hospital

# Create your views here.


def DoctorSearchPage(request):
    return render(request, 'Doctor/doctor_search_page.html')

def DoctorAskQuestionHandler(request, doctor_id):
    question = request.POST.get('question', '')
    DoctorQuery.objects.create(
        user = request.user,
        doctor = Doctor.objects.get(id = doctor_id),
        question = question
    )
    messages.success(request, 'Your query has been submitted successfully.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
        context['educations'] = DoctorEducation.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
        context['experiences'] = DoctorExperience.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
        context['queries'] = DoctorQuery.objects.filter(doctor = doctor, is_deleted = False, is_active=True).exclude(answer = '')
        context['doctor_reviews'] = DoctorReview.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
        if len(context['doctor_reviews']) > 0:
            context['rating_percentage'] = doctor.get_doctor_rating_percentage(reviews=context['doctor_reviews'])
        else:
            context['rating_percentage'] = 100

        return render(request, 'Doctor/doctor_view_profile.html', context)