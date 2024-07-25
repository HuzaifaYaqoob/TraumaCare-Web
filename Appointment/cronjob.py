

from Appointment.models import Appointment
from datetime import datetime, timedelta
from Administration.models import PhoneMessage


def expirePassedAppointments():
    time_now = datetime.now()
    one_hour = timedelta(hours=1)
    one_hour_before = time_now - one_hour
    apps = Appointment.objects.filter(
        date__lte = time_now.strftime('%Y-%m-%d'),
        start_time = one_hour_before,
        status__in = ["Pending", "Booked", "Confirmed"]
    )
    apps.update(status = "Expired")
    for appointment in apps:
        doctor_name = appointment.doctor.name
        patient_name = appointment.appointment_group.user.full_name

        app_date = appointment.date.strftime('%B %d, %Y')
        app_time = appointment.start_time.strftime('%I:%M %p')

        # Send Message to patient
        PhoneMessage.objects.create(
            phone_number = appointment.appointment_group.user.mobile_number,
            sms_type = 'ExpiredAppointment',
            text = f"Your appointment with Dr. {doctor_name} on {app_date} at {app_time} has expired due to non-attendance. Please reschedule via TraumaCare.",
        )
        # Send Message to Doctor
        PhoneMessage.objects.create(
            phone_number = appointment.doctor.mobile_number,
            sms_type = 'ExpiredAppointment',
            text = f"The appointment with {patient_name} on {app_date} at {app_time} has expired due to non-attendance. - TraumaCare",
        )
        if appointment.appointment_location == 'InPerson' and appointment.doct_hospital:
            # Send Message to Hospital
            PhoneMessage.objects.create(
                phone_number = appointment.doct_hospital.phone,
                sms_type = 'ExpiredAppointment',
                text = f"The appointment with Dr. {doctor_name} and {patient_name} on {app_date} at {app_time} has expired due to non-attendance. - TraumaCare",
            )
