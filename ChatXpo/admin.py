from django.contrib import admin

from ChatXpo.models import ChatMessage, XpoChat
# Register your models here.

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'chat',
        'display_content',
        'message_type',
    ]