


from rest_framework import serializers

from .models import Profile
from Doctor.models import Doctor


class GetUserProfiles(serializers.ModelSerializer):

    profile_label = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, profile):
        return f"{profile['profile_image']}"

        

    def get_profile_label(self, profile):
        return profile["profile_type"]

    class Meta:
        model = Profile
        fields = ['id', 'profile_type', 'profile_image', 'full_name', 'is_selected', 'profile_label']
        # 'email'

class GetMyDashboardActiveProfile(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, profile):
        return f'{profile.profile_image}'
    
    class Meta:
        model = Profile
        fields = ['profile_image', 'full_name', 'profile_label', 'email']