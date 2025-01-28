

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


from Trauma.models import Speciality, Disease
from Administration.models import PageAnalytics
from Trauma import serializers as TraumaSerializer
from Doctor import serializers as DoctorSerializer
from Doctor.models import Doctor

@api_view(['GET'])
@permission_classes([AllowAny])
def page_load_analytics(request, id):
    try:
        page_analytic = PageAnalytics.objects.get(id = id)
    except Exception as err:
        return Response({
            'message' : str(err),
            'id' : id,
        })
    
    page_analytic.urls = page_analytic.urls + ' --- Page Loaded'
    page_analytic.save()

    return Response({
            'Done' : 'True'
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_specialities(request):
    specialities = Speciality.objects.filter(
        is_deleted = False,
        is_active = True
    )
    serialized = TraumaSerializer.SpecialitiesSerializer(specialities, many=True)
    return Response({
        'status' : True,
        'status_code' : 200,
        'response' : {
            'count' : len(specialities),
            'specialities' : serialized.data,
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_speciality_doctors(request, spaciality_slug):
    try:
        speciality = Speciality.objects.get(slug = spaciality_slug,)
    except:
        return Response({
            'status' : False,
            'status_code' : 400,
            'response' : {
                'message' : 'Speciality Not Found',
                'error' : 'Speciality Not Found',
            }
        })
    
    docts = Doctor.objects.filter(
        is_active = True,
        is_deleted = False,
        doctor_specialities__speciality = speciality
    )
    serialized = DoctorSerializer.DoctorSpecialitySerializer(docts, many=True)
    return Response({
        'data' : serialized.data,
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_diseases(request):
    diseases = Disease.objects.filter(
        is_deleted = False,
        is_active = True
    )
    serialized = TraumaSerializer.DiseaseSerializer(diseases, many=True)
    return Response({
        'status' : True,
        'status_code' : 200,
        'response' : {
            'count' : len(diseases),
            'diseases' : serialized.data,
        }
    })

