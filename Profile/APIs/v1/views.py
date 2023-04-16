

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
            'count' : len(data),
            'data' : data,
        }
    }, status=status.HTTP_200_OK)