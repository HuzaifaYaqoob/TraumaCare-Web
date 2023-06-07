

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# Importing Models 
from Profile.models import Profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserGeneralProfileData(request):

    try:
        general_profile = Profile.objects.get(
            profile_type = 'Patient',
            user = request.user,
        )
        if general_profile.is_deleted:
            raise Exception('Sorry! This profile already has been deactivated')

    except Exception as err:
        return Response({
            'status' : False,
            'status_code' : 404,
            'request' : {

            },
            'response': {
                'message' : 'Profile does not exists',
                'error_message' : str(err),
            }
        }, status=status.HTTP_404_NOT_FOUND)
    
    else:
        if not general_profile.is_active:
            return Response({
                'status' : False,
                'status_code' : 400,
                'status_code_text' : 'USER_PROFILE_IS_INACTIVE',
                'request' : {

                },
                'response': {
                    'message' : 'Profile is not active',
                    'error_message' : 'User Profile is not Active, Please activate first',
                }
            }, status=status.HTTP_400_BAD_REQUEST)


        return Response({
            'status' : True,
            'status_code' : 200,
            'status_code_text' : 'USER_PROFILE_DATA',
            'request' : {

            },
            'response': {
                'message' : 'Authenticated user data',
                'error_message' : None,
                'user_profile' : {
                    'full_name' : f'{general_profile.full_name}',
                    'profile_image' : f'{general_profile.image_full_path}',
                    'dial_code' : f'{request.user.dial_code}',
                    'mobile_number' : f'{request.user.mobile_number}',
                }
            }
        }, status=status.HTTP_200_OK)