

from Trauma.models import Speciality

import random

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


def Locations_context_processors(request):
    context = {}

    context['countries'] = []

    return context