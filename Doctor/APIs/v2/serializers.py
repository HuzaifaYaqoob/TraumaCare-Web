


from rest_framework import serializers
from django.conf import settings
from Doctor.models import Doctor, DoctorWithHospital
from datetime import datetime, timedelta

class DeviceHomePageDoctorsSerializer(serializers.ModelSerializer):
    sp = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

    def get_sp(self, doctor):
        return doctor.heading[:50]


    def get_img(self, doctor):
        if doctor.profile_image:
            return f'{settings.THIS_APPLICATION_URL}{doctor.profile_image}'


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

    class Meta:
        model = DoctorWithHospital  
        fields = [
            'id',
            'name',
            'address',
        ]

class DoctorSingleProfileGet(serializers.ModelSerializer):
    sp = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    hospitals = serializers.SerializerMethodField()

    def get_hospitals(self, doctor):
        return DoctorWithHospitalViewProfileSerializer(DoctorWithHospital.objects.filter(doctor = doctor, is_deleted = False, is_active = True), many=True).data

    def get_sp(self, doctor):
        return doctor.heading


    def get_img(self, doctor):
        if doctor.profile_image:
            return f'{settings.THIS_APPLICATION_URL}{doctor.profile_image}'


    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'sp',
            'img',
            'desc',
            'hospitals',
        ]
