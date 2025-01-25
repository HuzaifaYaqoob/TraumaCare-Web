
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from Product.models import Product, ProductStock
import json
from urllib.parse import unquote
from Administration.Constant.site import get_site_settings



@api_view(['POST'])
@permission_classes([AllowAny])
def CalculateCart(request):
    cookie_data = request.COOKIES.get('CartItems', '')
    if cookie_data:
        decoded_data = unquote(cookie_data)
        CartItems = json.loads(decoded_data)
    else:
        CartItems = []
    
    site_settings = get_site_settings()
    data = []
    subtotal = 0
    discount_applied = 0
    platform_fee = site_settings['PHARMACY_PLATFORM_FEE'] * len(CartItems)
    delivery_charges = 149
    grand_total = 0

    for item in CartItems:
        try:
            product = Product.objects.get(id = item['id'])
            stock = ProductStock.custom_objects.filter(product = product, location__id = item['location_stock'], is_active=True, is_deleted=False).order_by('-created_at').first()
            
        except Exception as err:
            print(err)
            pass
        else:
            quantity = int(item['quantity'])
            images = product.product_all_images
            image = None
            if len(images) > 0 and images[0].image:
                image = images[0].image.url
            subtotal += stock.final_price * quantity
            if stock.discount:
                discount_applied += (stock.price - stock.final_price) * quantity

            data.append({
                'id' : product.id,
                'slug' : product.slug,
                'name' : product.name,
                'location_id' : stock.location.id,
                'location_name' : stock.location.name,
                'store_name' : product.store.name,
                'price' : round(stock.price, 2),
                'final_price' : round(stock.final_price, 2),
                'discount' : stock.discount,
                'image' : product.cover_image,
                'quantity' : quantity,
            })

    grand_total = (subtotal - discount_applied) + platform_fee + delivery_charges

    return Response({
        'data' : data,
        'subtotal' : round(subtotal, 2),
        'discount_applied' : round(discount_applied, 2),
        'platform_fee' : platform_fee,
        'delivery_charges' : round(delivery_charges, 2),
        'grand_total' : round(grand_total, 2)
    })