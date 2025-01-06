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
    context['other_locations'] = ProductStock.objects.filter(product = product).exclude(location = location)
    return render(request, 'Medicine/SingleMedicineViewPage.html', context)