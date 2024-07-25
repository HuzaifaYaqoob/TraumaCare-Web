from django.db import models

# Create your models here.


from uuid import uuid4
from Authentication.models import User
class Question(models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    title = models.CharField(max_length=999)
    description = models.TextField()

    slug = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_questions')

    votes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    is_repost = models.BooleanField(default=False)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        title = self.title
        title = title.replace(' ', '-').replace('/', '-').replace('--', '-')
        title = title.lower()
        self.slug = f'{title}-{self.id}'
        super().save(*args, **kwargs)

class Answer(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answers')
    answer = models.TextField()

    votes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answer_comments')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_comments')
    comment = models.TextField()

    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reaction(models.Model):
    REACTION_CHOICE = (
        ('Vote', 'Vote'),
        ('Downvote', 'Downvote'),
    )
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reactions')

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_reactions', null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_reactions', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reactions', null=True, blank=True)

    reaction = models.CharField(max_length=999, choices=REACTION_CHOICE, default='Vote')
    rank = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)