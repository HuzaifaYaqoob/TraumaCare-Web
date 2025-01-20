from django.shortcuts import render, redirect

from Product.models import Product, ProductStock
from Pharmacy.models import Store, StoreLocation
from django.contrib import messages

from django.db.models import Q, OuterRef, Subquery

# Create your views here.


def productDetailPage(request):
    return render(request, 'Product/product_details.html')


def ProductSearchpage(request):
    return render(request, 'Product/SingleMedicineViewPage.html')

def SingleMedicineViewPage(request, product_slug):
    location_id = request.GET.get('selected_location', None)

    try:
        product = Product.objects.filter(
            is_deleted = False,
            is_active = True,
            is_blocked = False,
            slug = product_slug,
        ).select_related(
                'Vendor', 'store',  'manufacturer', 'treatment_type', 'product_form', 'product_type',
            ).prefetch_related(
                'sub_category', 'sub_category__category', 'product_images', 'product_stocks', 'product_stocks__location'
            )[0]
    except Exception as err:
        print(err)
        messages.error(request, 'Invalid Page!')
        return redirect('PharmacyLandingPage')


    # location_stock = ProductStock.custom_objects.select_related('location').filter(product = product, location__id = location_id, is_active = True, is_deleted = False).order_by('-created_at').first()
    
    context = {}

    prod_sub_categories = product.sub_category.all()
    if len(prod_sub_categories) > 0:
        first_cat = prod_sub_categories[0]
        context['product_sub_category'] = first_cat
        context['product_main_category'] = first_cat.category.all()[0]
    
    context['product'] = product
    context['location_stock'] = product.lowest_rate_location(location_id=location_id)

    # other_locations = ProductStock.custom_objects.filter(product = product).exclude(Q(id = location_stock.id if location_stock else '1') | Q(final_price = location_stock.final_price if location_stock else '1')).order_by('final_price')[:3]
    # other_locations_data = []
    # for location_stock in other_locations:
    #     other_locations_data.append({
    #         'location_name' : location_stock.location.name, 'location_id' : location_stock.location.id,
    #         'price' : location_stock.price, 'final_price' : location_stock.final_price, 'discount' : location_stock.discount, 'slug' : location_stock.product.slug,
    #         'lat' : location_stock.location.lat, 'lng' : location_stock.location.lng,
    #     })
    # context['other_locations'] = other_locations_data

    other_medicines = Product.objects.filter(
        Q(sub_category__in = product.sub_category.all()) |
        Q(product_form = product.product_form) |
        Q(product_type = product.product_type) |
        Q(formulation = product.formulation) |
        Q(treatment_type = product.treatment_type),
        is_active=True, is_deleted=False, is_blocked=False,
    ).select_related('store').prefetch_related(
        'product_images',
        'product_stocks',
        'product_stocks__location',
    ).distinct().order_by('?')[:10]

    context['medicines'] = other_medicines

    # context['storeMedicines'] = Product.objects.filter(
    #     store = product.store,
    #     is_active=True, is_deleted=False, is_blocked=False,
    # ).distinct().order_by('?')[:10]

    return render(request, 'Medicine/SingleMedicineViewPage.html', context)