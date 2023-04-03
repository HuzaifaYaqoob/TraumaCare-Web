

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


from Trauma.models import Speciality, Disease
from Trauma import serializers as TraumaSerializer

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