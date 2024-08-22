


from rest_framework import serializers
from django.conf import settings
from Doctor.models import Doctor

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

class DoctorSingleProfileGet(serializers.ModelSerializer):
    sp = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()

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
        ]
