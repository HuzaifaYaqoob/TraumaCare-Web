


from rest_framework import serializers
from django.conf import settings
from Doctor.models import Doctor, DoctorWithHospital
from datetime import datetime, timedelta
from Appointment.models import Appointment
from Profile.models import Profile

class DeviceHomePageDoctorsSerializer(serializers.ModelSerializer):
    sp = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    def get_sp(self, doctor):
        return doctor.heading[:50]


    def get_img(self, doctor):
        if doctor.profile_image:
            return f'{doctor.profile_image}'


    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'sp',
            'img',
        ]


class DoctorWithHospitalViewProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='hospital.name')
    address = serializers.CharField(source='location.name')
    fee_range = serializers.SerializerMethodField()

    def get_fee_range(self, hospital):
        return hospital.fee_range


    class Meta:
        model = DoctorWithHospital  
        fields = [
            'id',
            'name',
            'address',
            'fee_range',
        ]

class DoctorSingleProfileGet(serializers.ModelSerializer):
    sp = serializers.CharField(source='heading')
    img = serializers.SerializerMethodField()

    def get_img(self, doctor):
        if doctor.profile_image:
            return f'{doctor.profile_image}'


    class Meta:
        model = Doctor
        fields = [
            'name',
            'sp',
            'img',
        ]

class DoctorAppointmentPatient(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
    img = serializers.SerializerMethodField()

    def get_img(self, profile):
        if profile.profile_image:
            return f'{profile.image_full_path}'

    class Meta:
        model = Profile
        fields = [
            'id',
            'name',
            'img'
        ]

class DoctorDashboardAppointmentsSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()

    def get_patient(self, appointment):
        return DoctorAppointmentPatient(appointment.appointment_group.patient_profile).data

    class Meta:
        model = Appointment
        fields = [
            'id',
            'status',
            'patient',
            # 'location'
        ]