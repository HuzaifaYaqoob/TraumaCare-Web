from django.shortcuts import render


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


from .models import VideoChat, VideoChatSetting
# from Profile.models import Profile, TeacherProfile
from Authentication.models import User
from .serializers import VideoChat_GetSerializer, VideoChatClasses

from datetime import datetime, timedelta


# @api_view(['POST'])
# def create_video_chat(request):
#     name = request.GET.get('name' , None)
#     tutor_slug = request.data.get('slug' , None)
#     date = request.data.get('date' , None)
#     start_time = request.data.get('start_time' , None)
#     end_time = request.data.get('end_time' , None)

#     if not request.user.is_authenticated:
#         return Response(
#             {
#                 'status' : False,
#                 'response' : {
#                     'message' : 'Authentication Failed',
#                     'error_message' : 'Invalid Token or Login Failed'
#                 }
#             }, status=status.HTTP_401_UNAUTHORIZED
#         )
    
#     if not date:
#         date = datetime.now().strftime("%Y-%m-%d")
    
#     if not end_time:
#         end_time = datetime.now() + timedelta(minutes=30)
#         end_time = end_time.strftime("%H:%M")

#     vid_chat = VideoChat.objects.create(
#         name=name,
#         host=request.user,
#         date = date,
#         start_time = start_time,
#         end_time = end_time
#     )
#     vid_chat.allowed_users.add(request.user)

#     try:
#         teacher = TeacherProfile.objects.get(slug = tutor_slug)
#     except Exception as err:
#         vid_chat.delete()
#         return Response(
#             {
#                 'status' : False,
#                 'response' : {
#                     'message' : 'Invalid Tutor ID',
#                     'slug' : tutor_slug,
#                     'error_message' : str(err)
#                 }
#             }, status=status.HTTP_400_BAD_REQUEST
#         )
#     else:
#         vid_chat.allowed_users.add(teacher.user)
#     vid_chat.save()

#     video_chat_setting = VideoChatSetting(
#         user = request.user,
#         video_chat = vid_chat,
#     )

#     video_chat_setting.save()

#     serialized = VideoChat_GetSerializer(vid_chat)

#     return Response(
#         {
#             'status' : True,
#             'response' : {
#                 'message' : 'Video Chat created successfully.',
#                 'data' : serialized.data,
#                 'error_message' : None
#             }
#         }, status=status.HTTP_201_CREATED
#     )

@api_view(['GET'])
def get_user_video_chats(request):
    video_chats = VideoChat.objects.filter(
        allowed_users = request.user
    )
    serialized = VideoChatClasses(video_chats, many=True, context={'request' : request})

    return Response(
        {
            'status' : True,
            'response' : {
                'data' : serialized.data
            }
        }
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_chat(request):
    vChat_id = request.GET.get('video_chat_id', None)

    if vChat_id is None:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : 'Invalid Data'
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        video_chat = VideoChat.objects.get(
            id=vChat_id, 
            is_deleted=False, 
            is_active=True,

        )
    except Exception as err:
        return Response(
            {
                'status' : False,
                'response' : {
                    'message' : str(err)
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )
    else:
        video_settings, created = VideoChatSetting.objects.get_or_create(video_chat=video_chat)
        if video_settings.lock_meeting and request.user not in video_chat.allowed_users.all():
            return Response(
                {
                    'status' : False,
                    'response' : {
                        'message' : 'Video Chat is locked'
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serialized_obj = VideoChat_GetSerializer(video_chat)
        return Response(
            {
                'status' : True,
                'response' : {
                    'data' : serialized_obj.data
                }
            },
            status=status.HTTP_200_OK
        )