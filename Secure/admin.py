from django.contrib import admin

from Secure.models import XpoKey, ApplicationReview, ChatInstructions, TraumacareApp
# Register your models here.


@admin.register(XpoKey)
class XpoKeyAdmin(admin.ModelAdmin):
  list_display = ['id', 'key', 'total_requests', 'token_used', 'completion_tokens', 'prompt_tokens', 'is_active', 'is_deleted',]

@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'email', 'rating', 'created_at' ]


@admin.register(ChatInstructions)
class ChatInstructionsAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'instruction', 'is_active',]


@admin.register(TraumacareApp)
class TraumacareAppAdmin(admin.ModelAdmin):
  ordering = ['-added_at']
  list_display = ['name', 'version', 'added_at']
