
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from ChatXpo.models import XpoChat, ChatMessage
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_chat_list(request):
    chat = XpoChat.objects.filter(
        user = request.user,
        is_active = True,
        is_deleted = False,
        is_blocked = False,
    ).order_by('-created_at')
    data = v1Serializers.XpoChatSerializer(chat, many=True).data
    return Response({
        'status' : 200,
        'status_code' : '200',
        'response' : {
            'message' : 'User chat list',
            'error_message' : '',
            'chat_list' : data
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_messages(request):
    chat_id = request.GET.get('chatId', None)
    chat = ChatMessage.objects.filter(
        chat__user = request.user,
        chat__uuid = chat_id,
        is_active = True,
        is_deleted = False,
        is_blocked = False,
    ).order_by('created_at')
    data = v1Serializers.ChatMessageSerializer(chat, many=True).data
    return Response({
        'status' : 200,
        'status_code' : '200',
        'response' : {
            'message' : 'User chat Messages',
            'error_message' : '',
            'chat_messages' : data
        }
    }, status=status.HTTP_200_OK)