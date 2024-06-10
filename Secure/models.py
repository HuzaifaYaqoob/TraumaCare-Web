from django.db import models
from uuid import uuid4
from django.utils.timezone import now
from Authentication.models import User
# Create your models here.


class XpoKey(models.Model):
    key = models.TextField(default='')

    completion_tokens = models.IntegerField(default=0)
    prompt_tokens = models.IntegerField(default=0)
    token_used = models.IntegerField(default=0)

    total_requests = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'

class ApplicationReview(models.Model):
    uuid = models.CharField(default=uuid4, editable=False, max_length=999)

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='user_application_reviews')
    name = models.CharField(max_length=225, default='')
    email = models.CharField(max_length=225, default='')

    rating = models.FloatField(default=0)
    text = models.TextField(default='')

    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return f'{self.uuid}'

class ChatInstructions(models.Model):
    uuid = models.CharField(default=uuid4, editable=False, max_length=999)
    name = models.CharField(max_length=999, default='')
    instruction = models.TextField(default='')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return f'{self.instruction}'