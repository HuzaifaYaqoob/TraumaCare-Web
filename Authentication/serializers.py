

from rest_framework import fields, serializers
from Authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'auth_token', 'id']
        