from django.contrib import admin
from django.db.models import Q, Value
# Register your models here.
from django.utils.html import mark_safe

from .models import Task, TaskAttachment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task', 'task_priority', 'date', 'task_status', 'assigned', 'creator',]

    exclude = ['created_by', 'start_time', 'end_time']

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
    task_priority.admin_order_field = 'priority'
    
    def task_status(self, task):
        color = 'Green'
        if task.status == 'Pending':
            color = 'Orange'
        elif task.status == 'In Progress':
            color = 'Blue'
        elif task.status == 'Completed':
            color = 'Green'
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{task.status}</span>')
    task_status.admin_order_field = 'status'
    
    def assigned(self, task):
        user = task.assigned_to
        div = f'<div style="display : flex;gap:10px"><span style="width: 50px;height:50px;border:1px solid lightgray;border-radius: 50%;background:url({user.profile_image}) no-repeat center center;background-size:cover"></span><p style="margin:0;padding:0;font-size:16px;white-space:nowrap;">{user.full_name}</p></div>'
        return mark_safe(div)
    assigned.admin_order_field = 'assigned_to'
    
    def creator(self, task):
        user = task.created_by
        div = f'<div style="display : flex;gap:10px"><span style="width: 50px;height:50px;border:1px solid lightgray;border-radius: 50%;background:url({user.profile_image}) no-repeat center center;background-size:cover"></span><span><p style="margin:0;padding:0;font-size:16px;white-space:nowrap;">{user.full_name}</p><p style="margin:0;padding:0;font-size:13px;font-weight:400">{task.created_at.strftime("%Y-%m-%d %H:%M %p")}</p></span></div>'
        return mark_safe(div)
    creator.admin_order_field = 'created_by'

    def task(self, task_obj):
        div = f'<div style=""><p style="margin:0;padding:0;font-size:13px;font-weight:400">{task_obj.task_type}</p><p style="margin:0;padding:0;font-size:16px">{task_obj.title}</p></div>'
        return mark_safe(div)
    creator.admin_order_field = 'title'
    
    def date(self, task):
        return mark_safe(f'<span><p style="white-space:nowrap;">{task.start_date.strftime("%Y-%m-%d")}</p><p>{task.start_date.strftime("%Y-%m-%d")}</p></span>')
    date.admin_order_field = 'end_date'
    
    def get_queryset(self, request):
        query_set = super().get_queryset(request)
        return query_set