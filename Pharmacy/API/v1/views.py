


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


from Pharmacy.models import Store, StoreLocation, StoreProductFile
from . import serializers
from .decorators import store_location_url_decorator

from PIL import Image
import pytesseract 
import cv2
import numpy as np
from io import BytesIO

from Trauma.ImageToText import ImageToText



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

# {
#     "ProductID": "16228",
#     "APIName": "GetProductByAlphabetV1",
#     "Slug": "spasler-neo-tablets-30s",
#     "Title": "Spasler Neo Tablets 135Mg (1 Box = 3 Strips) (1 Strip = 10 Tablets)",
#     "Slug1": "spasler-neo-tablets-30s",
#     "SalePercent": "0",
#     "Highlights": "",
#     "ProductImage": "https://dvago-assets.s3.ap-southeast-1.amazonaws.com/dvago-products-images/spasler-neo-tablets-30s.webp",
#     "Category": "Medicine",
#     "Brand": "AGP PHARMA",
#     "Price": "420",
#     "SalePrice": "420",
#     "ShopifyProductID": "1000000011126",
#     "VariationTitle": "Box",
#     "unitpercase": "30",
#     "AvailableQty": "2",
#     "MaxOrder": "20",
#     "Description": "Buy SPASLER NEO 135 MG TABLETS from AGP PHARMA and get it delivered at your door step only from Dvago",
#     "Variations": "Box",
#     "DiscountPrice": "399",
#     "DiscountAmount": "21",
#     "ParentCategory": "Consumer",
#     "PrescriptionRequired": "True",
#     "NoofStrips": "3",
#     "MaxStripOrder": "60",
#     "SaleStripPrice": "140",
#     "StripAvailableQty": "7",
#     "DiscountStripPrice": "133",
#     "DiscountStripAmount": "7",
#     "MetaTitle": "Spasler Neo Tablets 30'S - Buy Online at DVAGO\u00ae",
#     "MetaDescription": "Buy Spasler Neo Tablets 30'S Online in Pakistan at DVAGO Pharmacy. Get Genuine Medicines & Products at Discounted Prices with Free Shipping. Order Now!",
#     "TotalTablets": "30",
#     "TotalStripTablets": "10",
#     "ParentCategory1": "",
#     "ParentCategorySlug": "",
#     "Usedfor": "Anti-Spasmodic",
#     "Variation": [
#         {
#             "Type": "Box",
#             "SalePrice": "420",
#             "DiscountPrice": "399",
#             "DiscountAmount": "21",
#             "TotalTablets": "30",
#             "AvailableQty": "2",
#             "MaxOrder": "20",
#             "NoofStrips": "3"
#         },
#         {
#             "Type": "Strip",
#             "SalePrice": "140",
#             "DiscountPrice": "133",
#             "DiscountAmount": "7",
#             "TotalTablets": "10",
#             "AvailableQty": "7",
#             "MaxOrder": "60",
#             "NoofStrips": "1"
#         }
#     ]
# },
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def save_file_columns(request, *args, **kwargs):
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_product_by_image(request, *args, **kwargs):
    images = request.FILES.getlist('images')
    if not images:
        return Response({'message': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)

    data = {}
    for image_file in images:

        img_obj = ImageToText(Image.open(image_file))
        data[image_file.name] = img_obj.get_text()
                
    return Response({
        'data': data,
        'count': len(images),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_store_locations(request, *args, **kwargs):
    locations = StoreLocation.objects.filter(store = request.store).values('uuid', 'name', 'address')
    
    return Response({
        'data' : list(locations),
        'count' : len(locations)
    })