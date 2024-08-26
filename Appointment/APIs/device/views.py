


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token


from Appointment.models import Appointment
from django.db.models import Q 
import random

from .serializers import GetMyAppointmentsSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyAppointments(request):
    apps = Appointment.objects.filter(appointment_group__user = request.user)

    return Response(GetMyAppointmentsSerializer(apps, many=True).data)