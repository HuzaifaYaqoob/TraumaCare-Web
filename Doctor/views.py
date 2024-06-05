from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from Doctor.models import Doctor, DoctorTimeSlots, DoctorWithHospital, DoctorReview, DoctorEducation, DoctorExperience, DoctorQuery

from Hospital.models import Hospital

from datetime import datetime, timedelta
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

def DoctorProfilePage(request, doctor_slug):
    try:
        doctor = Doctor.objects.get(
            slug = doctor_slug,
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
        context['educations'] = DoctorEducation.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
        context['experiences'] = DoctorExperience.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
        context['queries'] = DoctorQuery.objects.filter(doctor = doctor, is_deleted = False, is_active=True).exclude(answer = '')
        context['doctor_reviews'] = DoctorReview.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
        if len(context['doctor_reviews']) > 0:
            context['rating_percentage'] = doctor.get_doctor_rating_percentage(reviews=context['doctor_reviews'])
        else:
            context['rating_percentage'] = 100

        doctor_specialities = doctor.doctor_specialities.all().values_list('speciality__id', flat=True)
        context['suggested'] = Doctor.objects.filter(
            doctor_specialities__speciality__id__in = doctor_specialities,
        ).distinct()

        online_availability_data = {}
        
        online_avas = DoctorTimeSlots.objects.filter(doctor = doctor, availability_type = 'Online', is_deleted = False, is_active=True)
        NewOnlineAva = []
        for onava in online_avas:
            available_intervals = onava.slots_interval
            if len(available_intervals) > 0:
                onava.model_slots_intervals = available_intervals
                NewOnlineAva.append(onava)

        if len(NewOnlineAva) > 0 :
            for online_ava in NewOnlineAva:
                date_data = online_ava.slot_next_date
                if len(date_data) > 0 and 'day_date' in date_data:
                    online_availability_data[date_data['day_date']] = online_availability_data.get(date_data['day_date']) or {'slots' : [], 'highest_discount' : {'discount' : online_ava.discount, 'day' : online_ava.day_abbr}}
                    online_availability_data[date_data['day_date']].update(date_data)
                    online_availability_data[date_data['day_date']]['slots'].append(online_ava)

                    if online_ava.discount > 0 and online_ava.discount > online_availability_data[date_data['day_date']]['highest_discount']['discount']:
                        dics = {'discount' : online_ava.discount, 'day' : online_ava.day_abbr}
                        online_availability_data[date_data['day_date']]['highest_discount'] = dics
            
            data = sorted(online_availability_data.items(), key = lambda x:datetime.strptime(x[0], '%Y-%m-%d'))
            online_availability_data = {data[0][0] : data[0][1]}

            context['online_availability'] = online_availability_data



        return render(request, 'Doctor/doctor_view_profile.html', context)