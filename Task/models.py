from django.db import models

# Create your models here.
from uuid import uuid4
from Authentication.models import User

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    )
    TASK_TYPE_CHOICES = (
        ('Task', 'Task'),
        ('FieldWork', 'FieldWork'),
        ('Meeting', 'Meeting'),
        ('LeadershipAndStrategic', 'LeadershipAndStrategic'),
        ('TechnologyAndDevelopment', 'TechnologyAndDevelopment'),
        ('MarketingAndSales', 'MarketingAndSales'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_task', null=True, blank=True)
    title = models.CharField(default='', max_length=999)
    description = models.TextField(default='')

    priority = models.CharField(default='Medium', max_length=999, choices=PRIORITY_CHOICES)
    task_type = models.CharField(default='Task', max_length=999, choices=TASK_TYPE_CHOICES)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(default='Pending', max_length=999, choices=STATUS_CHOICES)

    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to_task')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='task_attachment')
    attachment = models.FileField(upload_to='TaskAttachments/%Y/%m/')

    def __str__(self):
        return self.task
