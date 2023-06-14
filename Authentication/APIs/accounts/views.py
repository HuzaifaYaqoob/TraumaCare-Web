

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# Importing Models 
from Profile.models import Profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfilesData(request):
    user = request.user

    try:
        if user.is_deleted:
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
        if not user.is_active:
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
        
        
        existing_profiles = []
        profiles = Profile.objects.filter(
            user = user,
            is_deleted = False,
            is_active = True,
            is_blocked = False
        )
        for profile in profiles:
            existing_profiles.append({
                'profile_type' : profile.profile_type,
                'profile_name' : profile.full_name,
            })


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
                    'email' : f'{user.email}',
                    'full_name' : f'{user.full_name}',
                    'profile_image' : f'{user.profile_image}',
                    'dial_code' : f'{user.dial_code}',
                    'mobile_number' : f'{user.mobile_number}',
                    'existing_profiles' : existing_profiles,
                }
            }
        }, status=status.HTTP_200_OK)