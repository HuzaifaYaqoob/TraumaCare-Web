


from rest_framework import serializers
from django.conf import settings
from Doctor.models import Doctor

class DeviceHomePageDoctorsSerializer(serializers.ModelSerializer):
    hd = serializers.CharField(source='heading')
    img = serializers.SerializerMethodField()


    def get_img(self, doctor):
        if doctor.profile_image:
            return f'{settings.THIS_APPLICATION_URL}{doctor.profile_image}'


    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'hd',
            'img',
        ]
