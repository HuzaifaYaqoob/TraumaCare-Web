

from Trauma.models import Speciality

def specialities_context_processor(request):
    specialities = Speciality.objects.filter(
        is_deleted = False, 
        is_active = True,
        svg_icon__isnull = False,
    ).exclude(svg_icon = '').order_by('rank')[:8]

    return {
        'specialities' : specialities
    }