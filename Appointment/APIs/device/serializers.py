

from rest_framework import serializers

from Appointment.models import Appointment

class GetMyAppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'name',
        ]
    

    def to_representation(self, appointment):
        data = super().to_representation(appointment)
        data['day'] = appointment.day_name
        data['date'] = appointment.date_prefix_zero
        return data