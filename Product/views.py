from django.shortcuts import render, redirect

from Product.models import Product, ProductStock
from Pharmacy.models import Store, StoreLocation
from django.contrib import messages

# Create your views here.


def productDetailPage(request):
    return render(request, 'Product/product_details.html')


def ProductSearchpage(request):
    return render(request, 'Product/SingleMedicineViewPage.html')

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
        location = product.lowest_rate_location()

    location_stock = ProductStock.custom_objects.filter(product = product, location = location, is_active = True, is_deleted = False).order_by('-created_at').first()
    
    context = {}

    prod_sub_categories = product.sub_category.all()
    if len(prod_sub_categories) > 0:
        first_cat = prod_sub_categories[0]
        context['product_sub_category'] = first_cat
        context['product_main_category'] = first_cat.category.all()[0]
    
    context['product'] = product
    context['location'] = location
    context['location_stock'] = location_stock

    other_locations = ProductStock.custom_objects.filter(product = product).exclude(id = location_stock.id).order_by('final_price')[:3]
    other_locations_data = []
    for location_stock in other_locations:
        product_all_images = location_stock.product.product_all_images
        other_locations_data.append({
            'location_name' : location_stock.location.name, 'location_id' : location_stock.location.id,
            'price' : location_stock.price, 'final_price' : location_stock.final_price, 'discount' : location_stock.discount,
            'lat' : location_stock.location.lat, 'lng' : location_stock.location.lng,
        })
    context['other_locations'] = other_locations_data
    context['medicines'] = Product.objects.filter(is_active=True, is_deleted=False, is_blocked=False).order_by('?')[:10]
    return render(request, 'Medicine/SingleMedicineViewPage.html', context)