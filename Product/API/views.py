
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from Product.models import Product, ProductStock
import json
from urllib.parse import unquote



@api_view(['POST'])
@permission_classes([AllowAny])
def CalculateCart(request):
    cookie_data = request.COOKIES.get('CartItems', '')
    decoded_data = unquote(cookie_data)
    # Parse JSON data to Python list
    CartItems = json.loads(decoded_data)
    data = []
    subtotal = 0
    discount_applied = 0
    platform_fee = 9
    delivery_charges = 149
    grand_total = 0

    for item in CartItems:
        try:
            product = Product.objects.get(slug = item['slug'])
            stock = ProductStock.custom_objects.get(id = item['location_stock'])
        except Exception as err:
            # print(err)
            pass
        else:
            quantity = int(item['quantity'])
            images = product.product_all_images
            image = None
            if len(images) > 0 and images[0].image:
                image = images[0].image.url
            subtotal +=  (stock.final_price * quantity)
            if stock.discount:
                discount_applied += stock.discounted_price * quantity

            data.append({
                'id' : product.id,
                'slug' : product.slug,
                'name' : product.name,
                'location_id' : stock.location.id,
                'location_name' : stock.location.name,
                'store_name' : product.store.name,
                'price' : stock.price,
                'final_price' : stock.final_price,
                'discount' : stock.discount,
                'image' : image,
            })

    grand_total = (subtotal - discount_applied) + platform_fee + delivery_charges

    return Response({
        'data' : data,
        'subtotal' : subtotal,
        'discount_applied' : discount_applied,
        'platform_fee' : platform_fee,
        'delivery_charges' : delivery_charges,
        'grand_total' : grand_total
    })