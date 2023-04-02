

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


from Trauma.models import Speciality
from Trauma.serializers import SpecialitiesSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_specialities(request):
    specialities = Speciality.objects.filter(
        is_deleted = False,
        is_active = True
    )
    serialized = SpecialitiesSerializer(specialities, many=True)
    return Response({
        'status' : True,
        'status_code' : 200,
        'response' : {
            'count' : len(specialities),
            'specialities' : serialized.data,
        }
    })