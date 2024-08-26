

from rest_framework import serializers

from Appointment.models import Appointment
from Doctor.models import Doctor
from django.conf import settings


class AppointmentDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
        ]
    
    def to_representation(self, doctor):
        data = super().to_representation(doctor)
        data['image'] = f'{settings.THIS_APPLICATION_URL}{doctor.profile_image}'
        return data

class GetMyAppointmentsSerializer(serializers.ModelSerializer):
    doctor = AppointmentDoctorSerializer()
    class Meta:
        model = Appointment
        fields = [
            'id',
            'name',
            'doctor'
        ]
    

    def to_representation(self, appointment):
        data = super().to_representation(appointment)
        # data['day'] = appointment.day_name
        data['date'] = appointment.date_prefix_zero
        data['time'] = [appointment.start_time_format, appointment.end_time_format]

        return data