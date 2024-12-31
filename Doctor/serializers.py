

from rest_framework import serializers

from .models import Doctor


class DoctorProfileSerializer(serializers.ModelSerializer):

    phone_number = serializers.SerializerMethodField()

    def get_phone_number(self, doctor):
        return doctor.phone_number

    class Meta:
        model = Doctor
        fields = ['id', 'email', 'name', 'heading', 'phone_number', 'working_since', 'online_availability']

class DoctorSpecialitySerializer(serializers.ModelSerializer):
    fee_range = serializers.ReadOnlyField()
    profile_image = serializers.ReadOnlyField()

    class Meta:
        model = Doctor
        fields = ['slug', 'name', 'heading', 'fee_range', 'profile_image']