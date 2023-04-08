

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createDoctorProfile(request):
    return Response({
        'status' : True,
        'status_code' : 200,
        'response' : {
            'message' : 'Doctor Profile created Successfully.',
            'data' : {}
        }
    }, status=status.HTTP_201_CREATED)

