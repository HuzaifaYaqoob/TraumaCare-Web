

from rest_framework import fields, serializers
from Authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'auth_token', 'id']
        