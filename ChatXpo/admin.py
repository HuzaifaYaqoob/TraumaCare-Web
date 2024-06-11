from django.contrib import admin

from ChatXpo.models import ChatMessage, XpoChat
# Register your models here.

@admin.register(XpoChat)
class XpoChatAdmin(admin.ModelAdmin):
    actions = ['chat_messages_delete']
    list_display = [
        'uuid',
        'user',
        'title',
        'is_active',
        'is_deleted',
        'is_blocked',
    ]


    def chat_messages_delete(modeladmin, request, queryset):
        for chat in queryset:
            ChatMessage.objects.filter(
                chat = chat
            ).delete()
            chat.delete()

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'chat',
        'role',
        'content',
    ]