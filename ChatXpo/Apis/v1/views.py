
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from ChatXpo.models import XpoChat
from ChatXpo.Apis.v1 import serializers as v1Serializers

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_chat(request):
    chat = XpoChat.objects.create(
        user = request.user
    )
    data = v1Serializers.XpoChatSerializer(chat).data
    return Response({
        'status' : 201,
        'status_code' : '201',
        'response' : {
            'message' : 'New Chat Created',
            'error_message' : '',
            'data' : data
        }
    }, status=status.HTTP_201_CREATED)