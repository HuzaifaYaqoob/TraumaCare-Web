

from email import message
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from Meet.models import VideoChat, VideoChatSetting
from Authentication.models import User
from uuid import uuid4
import ollama
import time
from threading import Thread
import asyncio

from ChatXpo.models import XpoChat, ChatMessage


@database_sync_to_async
def get_user_chat(id):
    try:
        chat = XpoChat.objects.get(uuid = id)
        return chat
    except XpoChat.DoesNotExist:
        return None

@database_sync_to_async
def get_chat_previous_messages(chat):
    return list(ChatMessage.objects.filter(
        chat = chat,
        is_active = True,
        is_deleted = False,
        is_blocked = False,
    ).order_by('created_at'))

@database_sync_to_async
def create_new_chat(chat, message_text):
    return ChatMessage.objects.create(chat = chat, question = message_text)


class AiChatBotSocket(AsyncWebsocketConsumer):

    # CONNECTED

    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            return

        self.video_chat_id = self.scope['url_route']['kwargs']['chat_id']
        try:
            self.chat = await get_user_chat(self.video_chat_id)
            if self.chat is None:
                raise Exception('Error')
        except Exception as err:
            print(err)
            pass
        else:
            self.channel_base = f'ai-chat-user-socket-{str(self.chat.id)}'
            await self.accept()
            await self.channel_layer.group_add(
                self.channel_base,
                self.channel_name
            )

            await self.channel_layer.group_send(
                self.channel_base,
                {
                    'type' : 'chat.message',
                    'data' : {
                        'type' : 'CONNECTED',
                        'message' : 'Connected to Video chat'
                    }
                }
            )
    
    # async def send_ai_chat_messages(self):
    #     """Yeh function async way me messages send karega har 3 second ke gap ke sath"""
    #     for i in range(5):
    #         await self.send_message({
    #             'type': 'AI_CHAT_MESSAGE',
    #             'data': {
    #                 'message': f'{i} ',
    #                 'stream': False,
    #                 'message_id': 'undefined',
    #             }
    #         })
    #         print(f'Sent: {i}')
    #         await asyncio.sleep(1) # Proper async delay


    async def receive(self, text_data=None, bytes_data=None):
        """Client se message receive karne ka function"""
        text_data = json.loads(text_data)
        r_type = text_data['type']

        types_ = {
            'CONSUMER_NEW_AI_CHAT_MESSAGE' : self.consumer_new_message,
        }

        if r_type in types_:
            await types_[r_type](text_data)
    
    
    @database_sync_to_async
    def update_message(self, msg_obj, answer):
        msg_obj.answer = answer
        msg_obj.save()

        
    async def send_message_to_consumer(self, response, user_text):
        new_chat_message = await create_new_chat(self.chat, user_text)
        print(new_chat_message)
        msg_text = ''
        for index, chunk in enumerate(response):
            msg = chunk['message']['content']
            msg_text = msg_text + msg
            data = {
                'type' : 'AI_CHAT_MESSAGE',
                'data' : {
                    'message' : msg,
                    'stream' : True,
                    'message_id' : str(new_chat_message.id),
                }
            }
            await self.send_message(data)
            print(f'Sent: {index}')
            # await asyncio.sleep(1)
        await self.update_message(new_chat_message, msg_text)
        
        


    async def consumer_new_message(self, message):
        """Agar naya AI message aaye toh yeh function call hoga"""
        print('*' * 50)
        data = message['data']
        message_text = data['message']
        print(message_text)

        previous_chat = []
        # Async message sending loop

        chat_messages = await get_chat_previous_messages(self.chat)
        print(chat_messages)

        for chat_msg in chat_messages:
            if chat_msg.role == 'assistant':
                previous_chat.append({'role' : 'assistant', 'content' : chat_msg.question })
            else:
                if chat_msg.question:
                    previous_chat.append({'role' : 'user', 'content' : chat_msg.question })
                if chat_msg.answer:
                    previous_chat.append({'role' : 'assistant', 'content' : chat_msg.answer })
            
        previous_chat.append({'role' : 'user', 'content' : message_text })
        print(previous_chat)

        try:
            response = ollama.chat(
                model="deepseek-r1",
                messages=previous_chat,
                stream=True,
            )
        except Exception as ex_error:
            data = {
                'type' : 'AI_CHAT_MESSAGE',
                'data' : {
                    'message' : 'Abhi is waqt OpenAI ki Key expire ho chuki hai, that"s why me koi response return nahi kr sakta',
                    'stream' : True,
                    'message_id' : 'undefined',
                }
            }
            await self.send_message(data)
        else:
            
            asyncio.create_task(self.send_message_to_consumer(response, message_text))
            

        print(response)
        print('*' * 50)

        
    async def disconnect(self, code):
        print('Video chat not active, disconnected', code)
        try:
            await self.channel_layer.group_discard(
                self.channel_base,
                self.channel_name
            )
        except:
            pass

    async def chat_message(self, event):
        await self.send(json.dumps(event['data']))

    async def send_message(self, message):
        """Yeh function WebSocket message bhejega via Channel Layer"""
        await self.channel_layer.group_send(
            self.channel_base,
            {
                'type': 'chat_message',
                'data': message
            }
        )








# class ActivatedVideoChat(WebsocketConsumer):

#     # NEW_CONNECTION_ACCEPTED
    

#     def connect(self):
#         self.user = self.scope['user']
#         self.video_chat_id = self.scope['url_route']['kwargs']['videochat_id']

#         try:
#             get_chat = VideoChat.objects.get(id=self.video_chat_id)
#         except:
#             get_chat = None
#         # if self.user.is_authenticated and get_chat is not None and self.user in get_chat.allowed_users.all():
#         if self.user.is_authenticated and get_chat is not None:
#             self.vidChat = get_chat
#             self.accept()
#             if self.user.username == get_chat.host.username:
#                 try:
#                     self.vidChat.paticipants.add(self.user)
#                     self.vidChat.save()
#                 except Exception as err:
#                     print('///////////// ERRORR :::: /////////////')
#                     print(err)
#                     pass
#             self.activated_vc_channel_base = f'active-video-chat-{self.video_chat_id}'

#             async_to_sync(self.channel_layer.group_add)(
#                 self.activated_vc_channel_base,
#                 self.channel_name
#             )

#     def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         r_type = data['type']

#         if r_type == 'NEW_CONNECTION_REQUEST':
#             async_to_sync(self.channel_layer.group_send)(
#                 f'ai-chat-user-socket-{self.video_chat_id}-{self.vidChat.host.username}',
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'CONNECTION_ACCEPTED':
#             self.new_connection_accepted(data)
#         elif r_type == 'CONNECTION_REJECTED':
#             self.connection_rejected(data)
#         elif r_type == 'ICE_CANDIDATE':
#             self.IceCandidate(data)
#         elif r_type == 'NEW_USER_JOINED_VIDEO_CHAT':
#             self.NewUserJoinedVideoChat(data)
#         elif r_type == 'NEW_USER_JOINED_VIDEO_CHAT_APPROVED':
#             self.NewUserJoinedVideoChatApproved(data)
#         elif r_type == 'CUSTOM_OFFER':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'CUSTOM_ANSWER':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'USER_LEFT_MEETING':
#             try:
#                 get_user = User.objects.get(username=self.user.username)
#                 self.vidChat.paticipants.remove(get_user)
#                 self.vidChat.save()
#             except Exception as err:
#                 print('///////////// ERRORR :::: /////////////')
#                 print(err)
#                 pass
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'CHAT_NEW_MESSAGE':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'USER_MUTED_HIS_SELF':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'SCREEN_SHARE_NEW_CONNECTION':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'SCREEN_SHARE_NEW_CONNECTION_ANSWER':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'SCREEN_ICE_CANDIDATE':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )
#         elif r_type == 'SETTINGS_CHANGE':
#             chat_id = data.get('chat', {}).get('id', None)
#             if chat_id:
#                 chat_settings, created = VideoChatSetting.objects.get_or_create(video_chat__id=chat_id)
#                 input_settings = data.get('message', {})

#                 if 'allow_chat' in input_settings:
#                     chat_settings.allow_chat = input_settings.get('allow_chat')
#                 if 'allow_rename' in input_settings:
#                     chat_settings.allow_rename = input_settings.get('allow_rename')
#                 if 'lock_meeting' in input_settings:
#                     chat_settings.lock_meeting = input_settings.get('lock_meeting')
#                 if 'share_screen' in input_settings:
#                     chat_settings.share_screen = input_settings.get('share_screen')
#                 if 'start_video' in input_settings:
#                     chat_settings.start_video = input_settings.get('start_video')
#                 if 'unmute' in input_settings:
#                     chat_settings.unmute = input_settings.get('unmute')
#                 if 'waiting_room' in input_settings:
#                     chat_settings.waiting_room = input_settings.get('waiting_room')
                    
#                 chat_settings.save()

#                 data['hello'] = 'updated'
#                 data['hello_msg'] = data.get('message', {'no' : 'message'})
#                 async_to_sync(self.channel_layer.group_send)(
#                     self.activated_vc_channel_base,
#                     {
#                         'type' : 'chat.message',
#                         'message' : data
#                     }
#                 )
#             else:
#                 data['type'] = 'ERROR_FOR_CHAT_ID'
#                 async_to_sync(self.channel_layer.group_send)(
#                     self.activated_vc_channel_base,
#                     {
#                         'type' : 'chat.message',
#                         'message' : data
#                     }
#                 )
#         elif r_type == 'WHITE_BOARD_DATA':
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : data
#                 }
#             )

#     def disconnect(self, code):
#         was_user_active = False
#         try:
#             get_user = User.objects.get(username=self.user.username)
#             if get_user in self.vidChat.paticipants.all():
#                 was_user_active = True
#                 self.vidChat.paticipants.remove(get_user)
#                 self.vidChat.save()
#             else :
#                 was_user_active = False
           
#         except Exception as err:
#             print('EERRR :: ', err)
#             pass

#         if was_user_active:
#             user_obj = {
#                 'username' : str(self.user.username),
#                 'email' : str(self.user.email),
#                 'full_name' : str(self.user.full_name),
#                 'auth_token' : str(self.user.auth_token),
#             }
#             async_to_sync(self.channel_layer.group_send)(
#                 self.activated_vc_channel_base,
#                 {
#                     'type' : 'chat.message',
#                     'message' : {
#                         'type' : 'USER_LEFT_MEETING',
#                         'user' : user_obj
#                     }
#                 }
#             )
#         print('disconnected', code)


#     def chat_message(self, event):
#         message = event['message']

#         self.send(json.dumps(message))

#     def new_connection_accepted(self, message):
#         username = message['requested']['username']
#         # try:
#             # get_user = User.objects.get(username=username)
#             # self.vidChat.allowed_users.add(get_user)
#             # self.vidChat.save()
#         # except Exception as err:
#         #     print(err)

#         async_to_sync(self.channel_layer.group_send)(
#             f'ai-chat-user-socket-{self.video_chat_id}-{username}',
#             {
#                 'type' : 'chat.message',
#                 'message' : message
#             }
#         )


#     def connection_rejected(self, message):
#         username = message['requested']['username']

#         async_to_sync(self.channel_layer.group_send)(
#             f'ai-chat-user-socket-{self.video_chat_id}-{username}',
#             {
#                 'type' : 'chat.message',
#                 'message' : message
#             }
#         )


#     def IceCandidate(self, message):
#         # username = message['send_to']['username']
#         async_to_sync(self.channel_layer.group_send)(
#             self.activated_vc_channel_base,
#             {
#                 'type' : 'chat.message',
#                 'message' : message
#             }
#         )

#     def NewUserJoinedVideoChat(self, message):
#         try:
#             get_user = User.objects.get(username=self.user.username)
#             self.vidChat.paticipants.add(get_user)
#             self.vidChat.save()
#         except Exception as err:
#             print('///////////// ERRORR :::: /////////////')
#             print(err)
#         async_to_sync(self.channel_layer.group_send)(
#             self.activated_vc_channel_base,
#             {
#                 'type' : 'chat.message',
#                 'message' : message
#             }   
#         )

#     def NewUserJoinedVideoChatApproved(self, message):
#         async_to_sync(self.channel_layer.group_send)(
#             self.activated_vc_channel_base,
#             {
#                 'type' : 'chat.message',
#                 'message' : message
#             }   
#         )