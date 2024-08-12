

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from Doctor.APIs.v2.serializers import DeviceHomePageDoctorsSerializer
from Doctor.models import Doctor
from django.db.models import Q

@api_view(['Get'])
@permission_classes([AllowAny])
def getHomePageDoctors(request):
    doctors = Doctor.objects.filter(
        doctor_timeslots__isnull = False,
        is_active = True,
        is_deleted = False,
        is_blocked = False
    )

    return Response({"data" : DeviceHomePageDoctorsSerializer(doctors, many=True).data}, status=status.HTTP_200_OK)