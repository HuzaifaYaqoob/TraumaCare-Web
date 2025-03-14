


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


from Pharmacy.models import Store, StoreLocation, StoreProductFile
from . import serializers
from .decorators import store_location_url_decorator


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@store_location_url_decorator
def upload_store_location_file(request, *args, **kwargs):
    file = request.data.get('file', None)
    file_object = StoreProductFile.objects.create(store = request.store, location = request.store_location, file = file,)
    return Response({
        'message' : 'File Uplaoded Successfully',
        'data' : serializers.StoreProductFileSerializer(file_object).data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_store_files(request, *args, **kwargs):
    files = StoreProductFile.objects.filter(store = request.store, location = request.store_location).order_by('-created_at')
    data = serializers.StoreProductFileSerializer(files, many=True)

    return Response({
        'count' : len(files),
        'data' : data.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_store_file_columns(request, *args, **kwargs):
    file_id = request.GET.get('file_id', None)
    if not file_id:
        return Response({'message' : 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    

    try:
        file = StoreProductFile.objects.get(id = file_id, store = request.store, location = request.store_location)
    except Exception as err:
        return Response({'message' : 'Invalid File ID', 'error' : str(err)}, status=status.HTTP_400_BAD_REQUEST)
    
    columns = file.get_file_columns()
    first_row = file.get_file_first_row()
    data = serializers.StoreProductFileSerializer(file)

    return Response({
        'data' : data.data,
        'columns' : columns,
        'first_row' : first_row
    })