

from Trauma.models import Speciality, Disease
from django.conf import settings
import random

def global_context_processor(request):
    return {
        'dashboard_url' : settings.DASHBOARD_REDIRECT_URL
    }


def specialities_context_processor(request):
    specialities = Speciality.objects.filter(
        is_deleted = False, 
        is_active = True,
        svg_icon__isnull = False,
    ).exclude(svg_icon = '')
    # .order_by('rank')[:8]

    specialities = list(specialities)
    random.shuffle(specialities)

    return {
        'specialities' : specialities[:8]
    }

def diseases_context_processor(request):
    diseases = Disease.objects.filter(
        is_deleted = False, 
        is_active = True,
        # svg_icon__isnull = False,
    )
    # .exclude(svg_icon = '')
    # .order_by('rank')[:8]

    diseases = list(diseases)
    random.shuffle(diseases)

    return {
        'diseases' : diseases
    }


def Locations_context_processors(request):
    context = {}

    context['countries'] = []

    return context