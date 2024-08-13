


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from Trauma.models import VerificationCode


from django.db.models import Q 

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
            otp = otp, 
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
    return Response({
        'status' : True,
        'message' : 'Code Verified',
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def HandleLogin(request):
    
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

        email = f'{username}-{mobile_number}@traumacare.pk'
        password = f'{username}-{mobile_number}'
        dial_code = '92'
        full_name = f'{full_name} '.split(' ')
        first_name = full_name[0]
        try:
            last_name = full_name[1]
        except:
            last_name = ''

        user = User(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
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
        VerificationCode.objects.create(
            user = user,
            otp_type = 'MOBILE_VERIFICATION'
        )
        return Response({
            'status' : True,
            'message' : 'OTP Sent Successfully',
        })