from django.db import models

# Create your models here.

from Authentication.models import User


class UserRequestLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user_logs')

    log_requests = models.PositiveIntegerField(default=0)


    method = models.CharField(max_length=100, default='')
    query_params = models.TextField(blank=True, null=True)
    script_name = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=500)
    wdgi_multithread = models.BooleanField(default=False)
    wdgi_multiprocess = models.BooleanField(default=False)
    remote_addr = models.CharField(max_length=999, blank=True, null=True)
    real_ip = models.CharField(max_length=999, blank=True, null=True)
    remote_host = models.CharField(max_length=999, blank=True, null=True)
    remote_port = models.CharField(max_length=100, blank=True, null=True)
    server_name = models.CharField(max_length=999, blank=True, null=True)
    server_port = models.CharField(max_length=100, blank=True, null=True)
    http_host = models.CharField(max_length=999, blank=True, null=True)
    http_connection = models.CharField(max_length=999, blank=True, null=True)
    http_cache_control = models.CharField(max_length=999, blank=True, null=True)
    http_sec_ch_ua = models.TextField(blank=True, null=True)
    http_sec_ch_ua_mobile = models.CharField(max_length=999, blank=True, null=True)
    http_sec_ch_ua_platform = models.CharField(max_length=999, blank=True, null=True)
    http_user_agent = models.CharField(max_length=999, blank=True, null=True)
    http_accept = models.CharField(max_length=999, blank=True, null=True)


    post_data = models.TextField(blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    response_status = models.IntegerField()
    response_time = models.FloatField()
    data = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.remote_addr} - {self.path} at {self.timestamp}"