

from rest_framework import serializers

from Appointment.models import Appointment

class GetMyAppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'name',
        ]