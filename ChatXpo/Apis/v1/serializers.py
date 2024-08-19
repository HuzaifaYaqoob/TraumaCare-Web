

from ChatXpo.models import XpoChat, ChatMessage
from rest_framework import serializers


class XpoChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = XpoChat
        fields = ['uuid', 'title']

class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = ['uuid', 'question', 'answer', 'message_type', 'created_at']

        # 'user_query', 
        # 'display_content', 