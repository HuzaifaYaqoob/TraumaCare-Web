
import json

from Administration.models import UserRequestLog
from datetime import datetime

from django.contrib.gis.geoip2 import GeoIP2

class TrackUserLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    

    def get_user_location(self, ip):
        try:
            g = GeoIP2()
            response = g.city(ip)
            return response
        except:
            return None
    

    def __call__(self, request):
        real_ip = request.META.get('HTTP_X_REAL_IP', None) or '2400:adc5:1e1:d400:7145:9821:b22f:7be9'

        user_loc = self.get_user_location(real_ip)
        if user_loc:
            request.country = user_loc.get('country_name', None)
            request.country_code = user_loc.get('country_code', None)
            request.state = user_loc.get('region', None)
            request.city = user_loc.get('city', None)
            if request.country_code == 'PK':
                request.country_flag = '/static/assets/Images/pk_flag.jpg'

        response = self.get_response(request)
        

        # restricted_paths = [
        #     '/admin/' not in request.META.get('PATH_INFO'),
        #     '/media/' not in request.META.get('PATH_INFO'),
        #     '/.env' not in request.META.get('PATH_INFO'),
        #     '/robots.txt' not in request.META.get('PATH_INFO'),
        #     '/Core/Skin' not in request.META.get('PATH_INFO'),
        #     '/wp-login.php' not in request.META.get('PATH_INFO'),
        #     '/.config' not in request.META.get('PATH_INFO'),
        #     '/.aws/config' not in request.META.get('PATH_INFO'),
        #     '/.aws' not in request.META.get('PATH_INFO'),
        #     '/_profiler/phpinfo' not in request.META.get('PATH_INFO'),
        #     '/config/aws.yml' not in request.META.get('PATH_INFO'),
        #     '/info.php' not in request.META.get('PATH_INFO'),
        #     '/.env.bak' not in request.META.get('PATH_INFO'),
        #     '/phpinfo.php' not in request.META.get('PATH_INFO'),
        #     '/phpinfo' not in request.META.get('PATH_INFO'),
        #     '/.aws/credentials' not in request.META.get('PATH_INFO'),
        #     '/geoserver/web/' not in request.META.get('PATH_INFO'),
        #     '/webui/' not in request.META.get('PATH_INFO'),
        #     '/password.php' not in request.META.get('PATH_INFO'),
        #     '/systembc/password.php' not in request.META.get('PATH_INFO'),
        #     '/files/' not in request.META.get('PATH_INFO'),
        #     'favicon.ico' not in request.META.get('PATH_INFO'),
        #     '.css' not in request.META.get('PATH_INFO'),
        # ]

        # if all(restricted_paths):
        #     log, created = UserRequestLog.objects.get_or_create(
        #         real_ip = real_ip,
        #         method = request.method,
        #         path = request.META.get('PATH_INFO', ''),
        #         response_status = response.status_code,
        #     )
        #     log.log_requests = log.log_requests + 1
        #     log.timestamp = datetime.now()

        #     newData = {}
        #     for key, val in request.META.items():
        #         if type(val) in [str, int, float, bool]:
        #             newData[key] = val

        #     try:
        #         log.data = json.dumps(newData)
        #     except:
        #         pass
        
        #     if user_loc:
        #         log.country = user_loc.get('country_name', None)
        #         log.city = user_loc.get('city', None)
        #         log.country_code = user_loc.get('country_code', None)
        #         log.lat = user_loc.get('latitude', None)
        #         log.lng = user_loc.get('longitude', None)
        #         log.postal_code = user_loc.get('postal_code', None)
        #         log.geo_data = json.dumps(user_loc)

        #     if request.user.is_authenticated:
        #         log.user = request.user
        #     log.save()

        return response