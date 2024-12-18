from django.contrib import admin

# Register your models here.

from .models import Question, Answer, Comment, Reaction


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'votes', 'downvotes']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment']


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['uuid',]