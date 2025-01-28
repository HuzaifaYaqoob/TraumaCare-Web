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
        doctor = Doctor.objects.filter(
            slug = doctor_slug,
            is_active = True,
            is_deleted = False
        ).prefetch_related(
            'doctor_medias',
            'doctor_reviews',
            'doctor_available_days',
            'doctor_hospital_timeslots',
        )[0]
    except:
        messages.error(request, 'Invalid Doctor Profile.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    context = {}
    context['doctor'] = doctor
    context['practicing_locations'] = doctor.doctor_hospital_timeslots.all()
    context['educations'] = DoctorEducation.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
    context['experiences'] = DoctorExperience.objects.filter(doctor = doctor, is_deleted = False, is_active=True)
    context['queries'] = DoctorQuery.objects.filter(doctor = doctor, is_deleted = False, is_active=True).exclude(answer = '')
    context['doctor_reviews'] = doctor.doctor_reviews.all()

    if len(context['doctor_reviews']) > 0:
        context['rating_percentage'] = doctor.get_doctor_rating_percentage(reviews=doctor.doctor_reviews.all())
    else:
        context['rating_percentage'] = 100

    doctor_specialities = doctor.doctor_specialities.all().values_list('speciality__id', flat=True)
    suggested = Doctor.objects.filter(
        is_active = True,
        is_deleted = False,
        is_blocked = False,
        doctor_specialities__speciality__id__in = doctor_specialities,
    ).exclude(id = doctor.id).prefetch_related(
        'doctor_medias',
        'doctor_reviews',
        'doctor_available_days',
        'doctor_timeslots',
    ).distinct()
    context['suggested'] = suggested[:4]
    context['lowest_rate_suggested'] = suggested.order_by('doctor_timeslots__fee')[:3]


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


    print('wellay 4')
    print(context['practicing_locations'])

    return render(request, 'Doctor/doctor_view_profile.html', context)