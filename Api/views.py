from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

import geopy.distance
import json
# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def get_location_distance(request):
    # http://localhost:8000/api/v1/get_location_distance/?my_coords=31.48457979046869,74.26311376936425&hospital_coords=[[31.467087898775222,74.3158206070887]]
    data = request.data
    # data = {
    #     "my_coords" : {
    #         'lat' : 31.48457979046869,
    #         'lng' : 74.26311376936425
    #     },
    #     'location_coords' : {
    #         '31.467087898775222,74.3158206070887' : '31.467087898775222,74.3158206070887',
    #         '31.467087898775222,74.3158206070887' : '31.467087898775222,74.3158206070887',
    #         '31.467087898775222,74.3158206070887' : '31.467087898775222,74.3158206070887',
    #         '31.467087898775222,74.3158206070887' : '31.467087898775222,74.3158206070887',
    #         '31.467087898775222,74.3158206070887' : '31.467087898775222,74.3158206070887',
    #     }
    # }
    my_coords = data.get('my_coords', None)
    location_coords = data.get('location_coords', None)

    if not my_coords or not location_coords:
        return Response({
            'message' : 'Invalid Data',
        }, status=status.HTTP_400_BAD_REQUEST)

    my_coords = [my_coords.get('lat', None), my_coords.get('lng', None)]
    distances = {}
    for key, cord in location_coords.items():
        if len(key) > 5 and len(cord) > 5:
            cord = cord.split(',')
            cord = [float(cord[0]), float(cord[1])]
            distance = geopy.distance.geodesic(my_coords, cord)
            distances[key] = round(distance.km, 2)

    return Response(distances, status=status.HTTP_200_OK)