

from ChatXpo.models import XpoChat, ChatMessage
from rest_framework import serializers


class XpoChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = XpoChat
        fields = ['uuid', 'title']

class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = ['uuid', 'user_query', 'user_output_urdu', 'display_content', 'message_type', 'created_at']