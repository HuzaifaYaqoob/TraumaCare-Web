

from Trauma.models import Speciality, Disease
from django.conf import settings
import random
from datetime import datetime

from Hospital.models import Hospital
from Appointment.models import AppointmentGroup, Appointment

def global_context_processor(request):
    str_query = '?'
    for key in request.GET:
        val = request.GET.get(key)
        str_query += f'{key}={val}&'
    
    return {
        'dashboard_url' : settings.DASHBOARD_REDIRECT_URL,
        'str_query' : str_query,
        'reviews_count' : [1,2,3,4,5]
    }


def specialities_context_processor(request):
    specialities = Speciality.objects.filter(
        is_deleted = False, 
        is_active = True,
        # svg_icon__isnull = False,
    )
    # .exclude(svg_icon = '')
    # .order_by('rank')[:8]

    specialities = list(specialities)
    random.shuffle(specialities)

    return {
        'specialities' : specialities
    }

def diseases_context_processor(request):
    diseases = Disease.objects.filter(
        is_deleted = False, 
        is_active = True,
        # svg_icon__isnull = False,
    ).order_by('name')
    # .exclude(svg_icon = '')
    # .order_by('rank')[:8]
    return {
        'diseases' : diseases
    }

def hospitals_context_processor(request):
    hospitals = Hospital.objects.filter(
        is_active = True,
        is_deleted = False,
        is_blocked = False,
    ).values('name', 'id')
    return {
        'hospitals' : hospitals
    }


def Locations_context_processors(request):
    context = {}

    context['countries'] = []

    return context

def appointments_context_processors(request):
    context = {}

    if request.user.is_authenticated:
        today_date = datetime.now()
        print('today_date')
        print(today_date)
        context['today_date_dddd'] = today_date
        context['user_appointments'] = Appointment.objects.filter(appointment_group__user = request.user, status__in = ["Pending", "Booked", "Confirmed"], date__gte = today_date.strftime("%Y-%m-%d"), start_time__gte = today_date.strftime("%H:%M:%S"), )
        if len(context['user_appointments']) > 0:
            context['lastest_appointments'] = context['user_appointments'].order_by('date', 'start_time')[0]
        
        context['user_appointments'] = context['user_appointments'].count()

    return context