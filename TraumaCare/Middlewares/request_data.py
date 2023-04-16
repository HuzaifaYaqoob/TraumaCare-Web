
from django.utils.deprecation import MiddlewareMixin
import json


def isDicObj(value):
    if type(value) == str and value.startswith('{') and value.endswith('}'):
        return True
    return False

def isList(value):
    if type(value) == str and value.startswith('[') and value.endswith(']'):
        return True
    return False



class RequestDataCustomMiddleware(MiddlewareMixin):
    

    def process_request(self, request):

        if request.POST:
            request.POST._mutable = True
            for index, key in enumerate(request.POST):
                value = request.POST.get(key, None)
                if value is None:
                    continue

                if isDicObj(value):
                    try:
                        value = json.loads(value)
                    except Exception as error:
                        pass
                    else:
                        request.POST[key] = value
        