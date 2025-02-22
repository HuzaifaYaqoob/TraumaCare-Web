
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from ChatXpo.models import XpoChat, ChatMessage
from ChatXpo.Apis.v1 import serializers as v1Serializers

from ChatXpo.Sockets.Constant.Query import askChatXpo

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
    try:
        chat = XpoChat.objects.get(uuid = chat_id)
    except Exception as err:
        return Response({
            'status' : 404,
            'status_code' : '404',
            'response' : {
                'message' : 'Chat Not Found',
                'error_message' : str(err),
            }
        }, status=status.HTTP_404_NOT_FOUND)

    try:
        chat_messages = ChatMessage.objects.filter(
            chat__user = request.user,
            chat = chat,
            is_active = True,
            is_deleted = False,
            is_blocked = False,
        ).exclude(answer = '').order_by('created_at')
        data = v1Serializers.ChatMessageSerializer(chat_messages, many=True).data
        return Response({
            'status' : 200,
            'status_code' : '200',
            'response' : {
                'message' : 'User chat Messages',
                'chat_messages' : data
            }
        }, status=status.HTTP_200_OK)
    except Exception as err:
        return Response({
            'message' : str(err)
        },)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_chat_widget_message(request, chatId):
    try:
        chat = XpoChat.objects.get(uuid = chatId)
    except Exception as err:
        return Response({
            'status' : 404,
            'status_code' : '404',
            'response' : {
                'message' : 'Chat Not Found',
                'error_message' : str(err),
            }
        }, status=status.HTTP_404_NOT_FOUND)
    
    query = request.data['query']

    chat_messages = ChatMessage.objects.filter(
        chat = chat,
        is_active = True,
        is_deleted = False,
        is_blocked = False,
    ).order_by('created_at')

    chats = []
    for chat_msg in chat_messages:
        if chat_msg.role == 'assistant':
            chats.append({'role' : 'assistant', 'content' : chat_msg.question })
        else:
            if chat_msg.question:
                chats.append({'role' : 'user', 'content' : chat_msg.question })
            if chat_msg.answer:
                chats.append({'role' : 'assistant', 'content' : chat_msg.answer })

    try:
        response = askChatXpo(
            user_query = query,
            previousQueries = chats,
            user = chat.user if chat.user else chat.user
        )
    except Exception as ex_error:
        response = 'Abhi is waqt OpenAI ki Key expire ho chuki hai, that"s why me koi response return nahi kr sakta'
        # return Response({
        #     'status' : 400,
        #     'status_code' : '400',
        #     'response' : {
        #         'message' : 'Something went wrong',
        #         'error_message' : str(ex_error),
        #     }
        # }, status=status.HTTP_400_BAD_REQUEST)

    ChatMessage.objects.create(chat = chat, question = query, answer = response,),

    return Response({
        'status' : 200,
        'response' : {
            'message' : response
        }
    }, status=status.HTTP_201_CREATED)