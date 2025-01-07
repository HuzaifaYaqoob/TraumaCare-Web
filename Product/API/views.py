
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddProductToCart(request, product_slug):
    pass