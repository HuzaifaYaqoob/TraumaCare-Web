from django.contrib import admin

from ChatXpo.models import ChatMessage, XpoChat
from django.db.models import Q, Count
from datetime import datetime, timedelta
# Register your models here.


class ChatMessagesInline(admin.TabularInline):
    model = ChatMessage

    fields = [
        'question',
        'answer'
    ]

    readonly_fields = ('question', 'answer')
    can_delete = False
    extra = 0

@admin.register(XpoChat)
class XpoChatAdmin(admin.ModelAdmin):
    actions = ['chat_messages_delete', 'delete_chats_with_zero_messages']
    list_display = [
        'uuid',
        'user',
        'title',
        'chat_messages',
        'is_active',
        'is_deleted',
        'is_blocked',
        'created_at',
    ]

    inlines = [
        ChatMessagesInline
    ]

    def chat_messages(self, chat):
        return chat.chat_messages.all().count()


    def chat_messages_delete(modeladmin, request, queryset):
        for chat in queryset:
            ChatMessage.objects.filter(
                chat = chat
            ).delete()
            chat.delete()


    def delete_chats_with_zero_messages(modeladmin, request, queryset):
        XpoChat.objects.annotate(
            messages = Count('chat_messages')
        ).filter(
            messages = 0,
            created_at__lt = (datetime.now() - timedelta(days = 1))
        ).delete()

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'chat',
        'question',
        'answer',
    ]