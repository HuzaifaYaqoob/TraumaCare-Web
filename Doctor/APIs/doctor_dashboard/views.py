

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from Doctor.APIs.doctor_dashboard.serializers import DeviceHomePageDoctorsSerializer, DoctorSingleProfileGet
from Doctor.models import Doctor, DoctorWithHospital, DoctorTimeSlots
from django.db.models import Q

from Appointment.models import Appointment, AppointmentGroup
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def getDoctorAppointments(request):
    doctor = request.user.has_doctor_profile
    if not doctor:
        return Response({'message' : 'Invalid Doctor'}, status=status.HTTP_404_NOT_FOUND)
    
    appointments = Appointment.objects.filter(
        doctor = doctor
    )

    return Response({
        'data' : DoctorSingleProfileGet(doctor).data
    }, status=status.HTTP_200_OK)


@api_view(['Get'])
@permission_classes([AllowAny])
def getDoctorHospitalDays(request, hospitalId):
    try:
        doct_hosp = DoctorWithHospital.objects.get(
            id = hospitalId,
            is_active = True,
            is_deleted = False,
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


@api_view(['GET'])
@permission_classes([AllowAny])
def getDoctorHospitalSlots(request, doctorId, hospitalId):
    selected_date = request.GET.get('selected_date', None)
    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
    else:
        selected_date = datetime.now()
    
    day_name = selected_date.strftime('%A')
    
    slots = DoctorTimeSlots.objects.filter(
        day__day = day_name,
        doctor__id = doctorId,
        doc_hospital__id = hospitalId
    )

    data = []
    today_date = datetime.now().date()

    for slot in slots:
        apps = Appointment.objects.filter(
            doctor = slot.doctor,
            date = selected_date,
            doct_hospital = slot.doc_hospital,
        ).exclude(
            status__in = ["Finished", "Cancelled", "Expired"]
        ).values_list('start_time', flat=True)

        appointment_times = [app_Time.strftime('%H:%M:00') for app_Time in apps]
        intervals = []
        slot_intervals = slot.slots_interval if today_date == selected_date.date() else slot.get_all_intervals
        for interval in slot_intervals:
            if interval[0] in appointment_times:
                # Setting True if Slot already reserved
                interval.append(True)

            intervals.append(interval)

        d = {
            'name' : slot.title,
            'id' : slot.id,
            'fee' : slot.final_price,
            'intervals' : intervals,
            'start' : slot.start_time_formated,
            'end' : slot.end_time_formated,
        }
        if len(intervals) == 0:
            # Message for Patient that doctor time has been passed
            d['msg'] = 'Doctor time has been passed'
        data.append(d)
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def BookAppointment_DoctorPage(request, doctorId):
    
    doct_hospital_id = request.data.get('doct_hospital', None)
    slot_id = request.data.get('slot_id', None)

    selected_date = request.data.get('selected_date', None)
    selected_time = request.data.get('selected_time', None)

    try:
        doctor = Doctor.objects.get(id = doctorId, is_deleted = False, is_blocked = False)
    except Exception as err:
        return Response({
            'message' : 'Invalid Doctor Profile',
            'error' : str(err),
        }, status=status.HTTP_404_NOT_FOUND)

    if not doctor.is_active:
        return Response({
            'message' : 'Doctor is not active'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if doct_hospital_id:
        try:
            doct_hospital = DoctorWithHospital.objects.get(id = doct_hospital_id)
        except Exception as err:
            return Response({
                'message' : 'Doctor is not available at this Hospital',
                'error' : str(err),
            }, status=status.HTTP_404_NOT_FOUND)

    try:
        selected_slot = DoctorTimeSlots.objects.get(id = slot_id)
    except Exception as err:
        return Response({
            'message' : 'Selected Slot is not Available',
            'error' : str(err),
            'id' : slot_id
        }, status=status.HTTP_404_NOT_FOUND)
    
    appt_grp = AppointmentGroup.objects.create(
        user = request.user,
    )

    s_t = datetime.strptime(selected_time, "%H:%M:00")
    end_time = timedelta(minutes=doctor.get_time_inverval)
    end_time = end_time + s_t
    appointment = Appointment.objects.create(
        appointment_group = appt_grp,
        doctor = doctor,
        name = f'Appointment with {doctor.name} at {f"{doct_hospital.hospital.name}, {doct_hospital.location.name}" if doct_hospital_id else "Online"}',
        date = selected_date,
        start_time = selected_time,
        end_time=end_time.strftime("%H:%M"),
        slot = selected_slot,
        fee = selected_slot.fee,
        discount = selected_slot.discount,
        service_fee = selected_slot.service_fee,
        bill = selected_slot.final_price,
        status = 'Booked',
        appointment_location = 'InPerson' if doct_hospital_id else 'Online',
        doct_hospital = doct_hospital if doct_hospital_id else None,
    )

    return Response({
        'message' : 'Your appointment is booked successfully'
    }, status=status.HTTP_201_CREATED)