from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

import geopy.distance
# Create your views here.


@api_view(['GET'])
@permission_classes([AllowAny])
def get_location_distance(request):
    # ?my_coords=31.48457979046869,74.26311376936425&hospital_coords=31.467087898775222,74.3158206070887
    my_coords = request.GET.get('my_coords', None)
    hospital_coords = request.GET.get('hospital_coords', None)

    if not my_coords or not hospital_coords:
        return Response({
            'message' : 'Invalid Data',
        }, status=status.HTTP_400_BAD_REQUEST)

    my_coords = [float(i) for i in my_coords.split(',')]
    hospital_coords = [float(i) for i in hospital_coords.split(',')]
    distance = geopy.distance.geodesic(my_coords, hospital_coords)

    return Response({
        'km': round(distance.km, 2),
        'miles' : round(distance.miles, 2)
        }, status=status.HTTP_200_OK)