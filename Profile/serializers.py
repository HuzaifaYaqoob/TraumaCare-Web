


from rest_framework import serializers

from .models import Profile
from Doctor.models import Doctor


class GetUserProfiles(serializers.ModelSerializer):

    profile_image = serializers.SerializerMethodField()
    profile_type = serializers.SerializerMethodField()

    def get_profile_image(self, profile):
        return f'{profile.profile_image}'

    def get_profile_type(self, profile):
        return f'{profile.profile_label}'

    class Meta:
        model = Profile
        fields = ['id', 'profile_type', 'profile_image', 'full_name', 'is_selected']
        # 'email'

class GetMyActiveProfile(serializers.ModelSerializer):
    profile_type = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, profile):
        return f'{profile.profile_image}'
    
    def get_profile_type(self, profile):
        return f'{profile.profile_label}'

    class Meta:
        model = Profile
        fields = ['id', 'profile_type', 'profile_image', 'full_name']