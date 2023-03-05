


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from django.db.models import Q 

from Authentication.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def vaidate_unique_user(request):
    username = request.data.get('username', '')
    email = request.data.get('email', '')
    dial_code = request.data.get('dial_code', '')
    mobile_number = request.data.get('mobile_number', '')

    users = User.objects.filter(
        Q(username = username) |
        Q(email = email) |
        Q(mobile_number = mobile_number, dial_code = dial_code) 
    )

    print(users)

    return Response({
        'status' : False,
        'request' : {

        },
        'response' : {

        }
    })

