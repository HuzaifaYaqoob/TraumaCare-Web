from django.contrib import admin

# Register your models here.
from django.utils.html import mark_safe

from .models import Task, TaskAttachment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task_priority', 'task_type', 'start_date', 'end_date', 'task_status', 'created_by', 'assigned_to', 'created_at']

    exclude = ['created_by']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def task_priority(self, task):
        color = 'Green'
        if task.priority == 'Medium':
            color = 'Orange'
        elif task.priority == 'High':
            color = 'Red'
        elif task.priority == 'Critical':
            color = 'Red'
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{task.priority}</span>')
    
    def task_status(self, task):
        color = 'Green'
        if task.status == 'Pending':
            color = 'Orange'
        elif task.status == 'In Progress':
            color = 'Blue'
        elif task.status == 'Completed':
            color = 'Green'
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{task.status}</span>')
    