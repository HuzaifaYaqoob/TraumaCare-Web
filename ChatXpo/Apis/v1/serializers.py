

from ChatXpo.models import XpoChat
from rest_framework import serializers


class XpoChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = XpoChat
        fields = ['uuid', 'title']