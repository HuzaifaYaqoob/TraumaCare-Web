
import json

from Administration.models import UserRequestLog

class TrackUserLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    

    def __call__(self, request):
        response = self.get_response(request)

        if '/admin/' not in request.META.get('PATH_INFO') and 'favicon.ico' not in request.META.get('PATH_INFO'):
            log = UserRequestLog.objects.create(
                method = request.method,
                query_params = request.META.get('QUERY_STRING', ''),
                script_name = request.META.get('SCRIPT_NAME', ''),
                path = request.META.get('PATH_INFO', ''),
                real_ip = request.META.get('HTTP_X_REAL_IP', ''),
                wdgi_multithread = request.META.get('wsgi.multithread', False),
                wdgi_multiprocess = request.META.get('wsgi.multiprocess', False),
                remote_addr = request.META.get('REMOTE_ADDR', ''),
                remote_host = request.META.get('REMOTE_HOST', ''),
                remote_port = request.META.get('REMOTE_PORT', ''),
                server_name = request.META.get('SERVER_NAME', ''),
                server_port = request.META.get('SERVER_PORT', ''),
                http_host = request.META.get('HTTP_HOST', ''),
                http_connection = request.META.get('HTTP_CONNECTION', ''),
                http_cache_control = request.META.get('HTTP_CACHE_CONTROL', ''),
                http_sec_ch_ua = request.META.get('HTTP_SEC_CH_UA', ''),
                http_sec_ch_ua_mobile = request.META.get('HTTP_SEC_CH_UA_MOBILE', ''),
                http_sec_ch_ua_platform = request.META.get('HTTP_SEC_CH_UA_PLATFORM', ''),
                http_user_agent = request.META.get('HTTP_USER_AGENT', ''),
                http_accept = request.META.get('HTTP_ACCEPT', ''),
                response_status = response.status_code,
                response_time = 1,
            )

            newData = {}
            for key, val in request.META.items():
                if type(val) in [str, int, float, bool]:
                    newData[key] = val


            try:
                log.data = json.dumps(newData)
            except:
                pass

            if request.user.is_authenticated:
                log.user = request.user
            log.save()

        return response