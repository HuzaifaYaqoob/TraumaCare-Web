


from rest_framework import serializers

from .models import Profile
from Doctor.models import Doctor


class GetUserProfiles(serializers.ModelSerializer):

    profile_image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_name(self, profile):
        if profile.first_name and profile.last_name:
            return f'{profile.first_name} {profile.last_name}'
        elif profile.full_name:
            return profile.full_name
        
        return ''

    def get_profile_image(self, profile):
        return f'{profile.profile_image}'

    class Meta:
        model = Profile
        fields = ['id', 'profile_type', 'profile_image', 'name', 'is_selected']
        # 'email'