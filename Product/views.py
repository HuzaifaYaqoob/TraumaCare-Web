from django.shortcuts import render, redirect

from Product.models import Product, ProductStock
from Pharmacy.models import Store, StoreLocation
from django.contrib import messages

# Create your views here.


def productDetailPage(request):
    return render(request, 'Product/product_details.html')

def SingleMedicineViewPage(request, product_slug):
    try:
        product = Product.objects.get(
            slug = product_slug,
            is_deleted = False,
            is_active = True,
            is_blocked = False
        )
    except:
        messages.error(request, 'Invalid Page!')
        return redirect('PharmacyLandingPage')

    location = request.GET.get('selected_location', None)
    if location:
        try:
            location = StoreLocation.objects.get(id = location)
        except:
            pass
    if not location:
        location = product.lowest_rate_location
    
    
    context = {}
    context['product'] = product
    context['location'] = location

    other_locations = ProductStock.objects.filter(product = product).exclude(location = location)
    other_locations_data = []
    for location_stock in other_locations:
        product_all_images = location_stock.product.product_all_images
        other_locations_data.append({
            'slug' : location_stock.product.slug,
            'name' : location_stock.product.name,
            'store_name' : location_stock.product.store.name,
            'location_name' : location_stock.location.name,
            'location_id' : location_stock.location.id,
            'price' : location_stock.price,
            'final_price' : location_stock.final_price,
            'discount' : location_stock.discount,
            'image' : product_all_images[0].image.url if len(product_all_images) > 0 else None
        })
    context['other_locations'] = other_locations_data
    return render(request, 'Medicine/SingleMedicineViewPage.html', context)