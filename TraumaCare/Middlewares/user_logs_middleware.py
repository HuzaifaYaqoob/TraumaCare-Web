
import json

from Administration.models import UserRequestLog
from datetime import datetime

class TrackUserLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    

    def __call__(self, request):
        response = self.get_response(request)

        restricted_paths = [
            '/admin/' not in request.META.get('PATH_INFO'),
            '/media/' not in request.META.get('PATH_INFO'),
            '/.env' not in request.META.get('PATH_INFO'),
            '/robots.txt' not in request.META.get('PATH_INFO'),
            '/Core/Skin' not in request.META.get('PATH_INFO'),
            '/wp-login.php' not in request.META.get('PATH_INFO'),
            '/.config' not in request.META.get('PATH_INFO'),
            '/.aws/config' not in request.META.get('PATH_INFO'),
            '/.aws' not in request.META.get('PATH_INFO'),
            '/_profiler/phpinfo' not in request.META.get('PATH_INFO'),
            '/config/aws.yml' not in request.META.get('PATH_INFO'),
            '/info.php' not in request.META.get('PATH_INFO'),
            '/.env.bak' not in request.META.get('PATH_INFO'),
            '/phpinfo.php' not in request.META.get('PATH_INFO'),
            '/phpinfo' not in request.META.get('PATH_INFO'),
            '/.aws/credentials' not in request.META.get('PATH_INFO'),
            '/geoserver/web/' not in request.META.get('PATH_INFO'),
            '/webui/' not in request.META.get('PATH_INFO'),
            '/password.php' not in request.META.get('PATH_INFO'),
            '/systembc/password.php' not in request.META.get('PATH_INFO'),
            '/files/' not in request.META.get('PATH_INFO'),
            'favicon.ico' not in request.META.get('PATH_INFO'),
        ]

        if all(restricted_paths):
            log, created = UserRequestLog.objects.get_or_create(
                real_ip = request.META.get('HTTP_X_REAL_IP', ''),
                method = request.method,
                path = request.META.get('PATH_INFO', ''),
                query_params = request.META.get('QUERY_STRING', ''),
                response_status = response.status_code,
                response_time = 1,
            )
            log.log_requests = log.log_requests + 1
            log.script_name = request.META.get('SCRIPT_NAME', '')
            log.wdgi_multithread = request.META.get('wsgi.multithread', False)
            log.wdgi_multiprocess = request.META.get('wsgi.multiprocess', False)
            log.remote_addr = request.META.get('REMOTE_ADDR', '')
            log.remote_host = request.META.get('REMOTE_HOST', '')
            log.remote_port = request.META.get('REMOTE_PORT', '')
            log.server_name = request.META.get('SERVER_NAME', '')
            log.server_port = request.META.get('SERVER_PORT', '')
            log.http_host = request.META.get('HTTP_HOST', '')
            log.http_connection = request.META.get('HTTP_CONNECTION', '')
            log.http_cache_control = request.META.get('HTTP_CACHE_CONTROL', '')
            log.http_sec_ch_ua = request.META.get('HTTP_SEC_CH_UA', '')
            log.http_sec_ch_ua_mobile = request.META.get('HTTP_SEC_CH_UA_MOBILE', '')
            log.http_sec_ch_ua_platform = request.META.get('HTTP_SEC_CH_UA_PLATFORM', '')
            log.http_user_agent = request.META.get('HTTP_USER_AGENT', '')
            log.http_accept = request.META.get('HTTP_ACCEPT', '')
            log.timestamp = datetime.now()
            log.save()

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