

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from Profile.models import Profile
from Profile.serializers import GetUserProfiles


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_sidebar_profiles(request):
    
    user_profiles = Profile.objects.filter(
        user = request.user,
        is_active = True,
        is_deleted = False,
        is_blocked = False
    ).order_by('-is_selected')

    data = GetUserProfiles(user_profiles, many=True).data
    return Response({
        'status' : True,
        'status_code' : 200,
        'response' : {
            'message' : 'Your all profiles',
            'error_message' : None,
            'count' : len(data),
            'data' : data,
        }
    }, status=status.HTTP_200_OK)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def switch_my_active_profile(request):
    profile_id = request.data.get('profile_id', None)
    if profile_id is None:
        return Response({
            'status' : False,
            'status_code' : 400,
            'response' : {
                'message' : 'Please provide profile_id',
                'error_message' : 'Missing Field',
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_profile = Profile.objects.get(
            id = profile_id
        )
    except Exception as error:
        return Response({
            'status' : False,
            'status_code' : 404,
            'response' : {
                'message' : 'Profile not found',
                'error_message' : str(error)
            }
        }, status=status.HTTP_404_NOT_FOUND)
    
    if user_profile.user != request.user:
        return Response({
            'status' : False,
            'status_code' : 403,
            'response' : {
                'message' : 'You are not allowed to switch this profile',
                'error_message' : 'UnAuthorized user to perform this action'
            }
        }, status=status.HTTP_403_FORBIDDEN)
    
    otherProfiles = Profile.objects.filter(
        is_selected = True
    )
    for p in otherProfiles:
        p.is_selected = False
        p.save()
    
    user_profile.is_selected = True
    user_profile.save()


    return Response({
        'status' : True,
        'status_code' : 200,
        'response' : {
            'message' : 'Profile Switched',
            'error_message' : None
        }
    }, status=status.HTTP_200_OK)