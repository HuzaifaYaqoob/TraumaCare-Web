


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from Trauma.models import VerificationCode


from django.db.models import Q 
import random
from Authentication.models import User



@api_view(['POST'])
@permission_classes([AllowAny])
def HandleOtpVerification(request):
    mobile_number = request.data.get('mobile_number', None)
    otp = request.data.get('otp', None)

    try:
        user = User.objects.get(mobile_number = mobile_number)
    except:
        return Response({
            'status' : False,
            'message' : 'Invalid User',
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        code = VerificationCode.objects.get(
            user = user, 
            code = otp, 
            is_used = False, 
            is_deleted = False, 
            is_expired = False
        )
    except:
        return Response({
            'status' : False,
            'message' : 'Invalid Code',
        }, status=status.HTTP_400_BAD_REQUEST)

    code.is_used = True
    code.is_expired = True
    code.save()
    user.is_active = True
    user.save()

    
    token = Token.objects.get_or_create(user = user)[0].key
    return Response({
        'status' : True,
        'message' : 'Code Verified',
        'token' : token,
        'name'  : user.full_name
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def HandleLogin(request):
    
    try:
        mobile_number = request.data.get('mobile_number', None)
        

        if not mobile_number or len(mobile_number) != 11 or not mobile_number.startswith('03'):
            return Response({
                'status' : False,
                'message' : 'Invalid Phone Number',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(mobile_number = mobile_number)
        except:
            full_name = request.data.get('full_name', None)
            if not full_name:
                return Response({
                    'status' : False,
                    'message' : 'Full name required',
                }, status=status.HTTP_400_BAD_REQUEST)

            username = full_name.replace(' ', '')
            keepChecking = True
            while keepChecking:
                try:
                    user = User.objects.get(username = username)
                except:
                    keepChecking = False
                else:
                    username = f'{username}-{random.randint(1000, 9999)}'

            email = f'{username}-{mobile_number}@traumaaicare.com'
            password = f'{username}-{mobile_number}'
            dial_code = '92'

            user = User(
                username = username,
                email = email,
                full_name = full_name,
                dial_code = dial_code,
                mobile_number = mobile_number
            )
            user.set_password(password)
            user.save()

            VerificationCode.objects.create(
                user = user,
                otp_type = 'MOBILE_VERIFICATION'
            )

            return Response({
                'status' : True,
                'message' : 'OTP Sent Successfully',
            })
        else:
            # Login User here.
            if user.is_deleted:
                return Response({
                    'status' : False,
                    'message' : 'You are not allowed to login with this Phone Number.',
                }, status=status.HTTP_400_BAD_REQUEST)

            VerificationCode.objects.create(
                user = user,
                otp_type = 'MOBILE_VERIFICATION'
            )
            return Response({
                'status' : True,
                'message' : 'OTP Sent Successfully',
            })

    except Exception as err:
        return Response({
            'status' : False,
            'message' : str(err),
        }, status=status.HTTP_400_BAD_REQUEST)