

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from Doctor.APIs.v2.serializers import DeviceHomePageDoctorsSerializer, DoctorSingleProfileGet
from Doctor.models import Doctor, DoctorWithHospital
from django.db.models import Q

from datetime import datetime, timedelta

@api_view(['Get'])
@permission_classes([AllowAny])
def getHomePageDoctors(request):
    doctors = Doctor.objects.filter(
        doctor_timeslots__isnull = False,
        is_active = True,
        is_deleted = False,
        is_blocked = False
    ).distinct('id')

    return Response({"data" : DeviceHomePageDoctorsSerializer(doctors, many=True).data}, status=status.HTTP_200_OK)

@api_view(['Get'])
@permission_classes([AllowAny])
def getDoctorProfile(request, doctorId):
    try:
        doctor = Doctor.objects.get(
            id = doctorId,
            is_active = True,
            is_deleted = False,
            is_blocked = False
        )
    except Exception as err:
        return Response({"error" : str(err), 'message' : 'Invalid Doctor ID'}, status=status.HTTP_404_NOT_FOUND)

    return Response({**DoctorSingleProfileGet(doctor).data}, status=status.HTTP_200_OK)


@api_view(['Get'])
@permission_classes([AllowAny])
def getDoctorHospitalDays(request, hospitalId):
    try:
        doct_hosp = DoctorWithHospital.objects.get(
            id = hospitalId,
            is_active = True,
            is_deleted = False,
            is_blocked = False
        )
    except Exception as err:
        return Response({"error" : str(err), 'message' : 'Invalid Hospital Instance Id'}, status=status.HTTP_404_NOT_FOUND)
    
    days_slots = []
    date_now = datetime.now()
    current_month = date_now.month
    for i in range(30):
        date = date_now + timedelta(days = i)
        data = {
            'day' : date.strftime("%a"),
            'date_format' : date.strftime("%Y-%m-%d"),
            'date' : date.strftime("%d"),
        }
        if current_month != date.month:
            data['month'] = date.strftime("%b")

        days_slots.append(data)
    
    return Response(days_slots, status=status.HTTP_200_OK)