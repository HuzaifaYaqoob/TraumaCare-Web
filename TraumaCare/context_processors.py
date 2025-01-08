

from Trauma.models import Speciality, Disease
from django.conf import settings
import random
from datetime import datetime

from Hospital.models import Hospital
from Trauma.models import City
from Appointment.models import AppointmentGroup, Appointment

from django.db.models import Q, Count
from django.contrib import messages
from ChatXpo.models import XpoChat, ChatMessage

import json
from urllib.parse import unquote

def global_context_processor(request):
    context = {}
    str_query = '?'
    for key in request.GET:
        val = request.GET.get(key)
        str_query += f'{key}={val}&'
    
    chat_id = None
    chat_widget_messages = []
    if request.user.is_authenticated:
        user_chat = XpoChat.objects.filter(
            user = request.user,
            is_active = True,
            is_deleted = False,
            is_blocked = False
        ).order_by('-created_at')
        if user_chat.exists():
            chat_id = user_chat.first().uuid
        else:
            newchat = XpoChat.objects.create(
                user = request.user, 
                title = 'Chat Widget Chat'
            )
            chat_id = newchat.uuid
            ChatMessage.objects.create(
                chat = newchat,
                question = f'User Name : {request.user.full_name}, User Email : {request.user.email}, phone : {request.user.mobile_number if request.user.mobile_number else "No Phone Number Yet"}',
                role = 'assistant',
            )

    
        chat_widget_messages = ChatMessage.objects.filter(chat__uuid = chat_id, is_deleted = False, is_blocked = False, is_active = True).exclude(role = 'assistant').order_by('created_at')
    
    if request.user.is_authenticated:
        authToken = request.user.auth_token.key
        context['authToken'] = authToken

    
    cookie_data = request.COOKIES.get('CartItems', '')
    decoded_data = unquote(cookie_data)
    # Parse JSON data to Python list
    CartItems = json.loads(decoded_data)
    print(CartItems)

    return {
        'settings' : settings,
        'dashboard_url' : settings.DASHBOARD_REDIRECT_URL,
        'str_query' : str_query,
        'reviews_count' : [1,2,3,4,5],
        'chat_widget_chat_id' : chat_id,
        'chat_widget_messages' : chat_widget_messages,
        'CartItems' : len(CartItems),
        **context
    }


def specialities_context_processor(request):
    specialities = Speciality.objects.filter(
        is_deleted = False, 
        is_active = True,
        # svg_icon__isnull = False,
    )
    # .exclude(svg_icon = '')
    # .order_by('rank')[:8]

    # specialities = list(specialities)
    # random.shuffle(specialities)

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
        'hospitals' : hospitals,
        'hospital_cities' : City.objects.filter(city_hospital_locations__hospital__isnull = False).distinct().annotate(hospital_count = Count('city_hospital_locations'))
    }


def Locations_context_processors(request):
    context = {}

    context['countries'] = []

    return context

def appointments_context_processors(request):
    context = {}

    if request.user.is_authenticated:
        today_date = datetime.now().date()
        current_time = datetime.now().time()

        context['user_appointments'] = Appointment.objects.filter(
            Q(appointment_group__user=request.user),
            Q(status__in=["Pending", "Booked", "Confirmed"]),
            Q(date=today_date, start_time__gte=current_time) | Q(date__gt=today_date)
        )
        if len(context['user_appointments']) > 0:
            context['lastest_appointments'] = context['user_appointments'].order_by('date', 'start_time')[0]
        
        context['user_appointments'] = context['user_appointments'].count()

    return context