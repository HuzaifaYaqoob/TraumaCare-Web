


from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q 


@api_view(['POST'])
def vaidate_unique_user(request):
    username = request.data.get('username', None)
    email = request.data.get('email', None)
    phone = request.data.get('phone', None)

    return Response({
        'status' : False,
        'request' : {

        },
        'response' : {

        }
    })

