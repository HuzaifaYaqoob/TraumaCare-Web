


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


from django.db.models import Q 

from Authentication.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def vaidate_unique_user(request):
    username = request.data.get('username', '')
    email = request.data.get('email', '')
    # dial_code = request.data.get('dial_code', '')
    mobile_number = request.data.get('mobile_number', '')

    users = User.objects.filter(
        Q(username = username) |
        Q(email = email) |
        Q(mobile_number = mobile_number) 
    )

    reserved_fields = []

    for user in users:
        if username and user.username == username:
            reserved_fields.append('username')

        if email and user.email == email:
            reserved_fields.append('email')

        if user.mobile_number == mobile_number:
            reserved_fields.append('mobile_number')

    return Response({
        'status' : False,
        'request' : {

        },
        'response' : {
            'reserved_fields' : reserved_fields
        }
    }, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def Signup(request):
    email = request.POST.get('email', None)
    username = request.POST.get('username', None)
    dial_code = request.POST.get('dial_code', None)
    mobile_number = request.POST.get('mobile_number', None)
    password = request.POST.get('password', None)
    confirm_password = request.POST.get('confirm_password', None)
    
    if not all([email, username, dial_code, mobile_number, password, confirm_password]):
        return Response({
            'status' : False,
            'status_code' : 400,
            'request' : {

            },
            'response': {
                'message' : 'Invalid Data',
                'error_message' : 'Following fields are required.',
                'fields' : [
                    'email',
                    'username',
                    'dial_code',
                    'mobile_number',
                    'password',
                    'confirm_password',
                ],
            }
        }, status=status.HTTP_200_OK)


    user = User.objects.create_user(
        username = username,
        password = password,
        email = email
    )
    user.dial_code = dial_code
    user.mobile_number = mobile_number
    user.save()

    return Response({
        'status' : True,
        'status_code' : 200,
        'request' : {

        },
        'response': {
            'message' : 'Verification OTP has been sent to your Phone Number, Please Verify!',
            'error_message' : None,
        }
    }, status=status.HTTP_200_OK)

