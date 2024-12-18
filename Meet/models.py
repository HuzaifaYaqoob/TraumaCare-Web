from django.db import models

from Authentication.models import User
from uuid import uuid4

from django.utils.timezone import now



class VideoChat(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, unique=True, editable=False, max_length=1000)
    name = models.CharField(max_length=1000, default='', null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True , related_name='video_chats')
    allowed_users = models.ManyToManyField(User, related_name='allowed_video_chats' )
    paticipants = models.ManyToManyField(User, related_name='participated_video_chats', blank=True)

    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=now)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.id)


class VideoChatMedia(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, unique=True, editable=False, max_length=1000)
    file = models.FileField(upload_to='video_chat_media')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_vchat_medias')
    video_chat = models.ForeignKey(VideoChat, on_delete=models.CASCADE , related_name='video_chat_medias')

    created_at = models.DateTimeField(auto_now_add=now)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.id)


    def get_video_chat_name(self):
        return self.video_chat.name if self.video_chat.name else 'No Name N/A'


class VideoChatSetting(models.Model):
    id = models.CharField(default=uuid4, primary_key=True, unique=True, editable=False, max_length=1000)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_vchat_settings')
    video_chat = models.ForeignKey(VideoChat, on_delete=models.CASCADE , related_name='video_chat_settings')

    lock_meeting = models.BooleanField(default=False)
    waiting_room = models.BooleanField(default=True)

    share_screen = models.BooleanField(default=False)
    allow_chat = models.BooleanField(default=False)
    unmute = models.BooleanField(default=False)
    start_video = models.BooleanField(default=False)
    allow_rename = models.BooleanField(default=False)

    muted_participant = models.ManyToManyField(User, related_name='muted_participants')


    def __str__(self):
        return str(self.id)

