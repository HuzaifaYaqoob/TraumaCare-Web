from django.shortcuts import render
from django.db.models import Q
from Product.models import Product, ProductStock
import json
from urllib.parse import unquote
# Create your views here.

def PharmacyLandingPage(request):
    context = {}
    medicines = Product.objects.filter(is_active=True, is_deleted=False, is_blocked=False).order_by('?')[:10]


    context['medicines'] = medicines
    return render(request, 'Pharmacy/pharmacy_landing.html', context)

def PharmacySearchPage(request):
    context = {}
    query = Q()
    searchQuery = request.GET.get('searchQuery', '')
    category = request.GET.get('category', None)


    if category:
        query.add(Q(sub_category__category__slug = category), query.connector)

    searchedProducts = Product.objects.filter(
        Q(name__icontains = searchQuery) |
        Q(sub_category__name__icontains = searchQuery) |
        Q(sub_category__category__name__icontains = searchQuery),
        is_active=True, is_deleted=False, is_blocked=False,
    ).filter(query).distinct()

    context['total_medicines'] = len(searchedProducts)
    context['medicines'] = searchedProducts[:28]
    return render(request, 'Pharmacy/pharmacy_search.html', context)

def PharmacyCartPage(request):
    cookie_data = request.COOKIES.get('CartItems', '')

    if cookie_data:
        decoded_data = unquote(cookie_data)
        CartItems = json.loads(decoded_data)
    else:
        CartItems = []
    data = []
    products = []
    categories = []
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
            print(err)
            pass
        else:
            categories.extend(list(product.sub_category.all().values_list('name', flat=True).distinct()))
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

    print(categories)
    similar_products = Product.objects.filter(
        sub_category__name__in = categories,
        is_active=True, is_deleted=False, is_blocked=False,
    ).distinct().exclude(slug__in=[item['slug'] for item in CartItems]).order_by('?')[:10]

    grand_total = (subtotal - discount_applied) + platform_fee + delivery_charges
    context = {
        'similar_products' : similar_products,
        'data' : data,
        'subtotal' : round(subtotal, 2),
        'discount_applied' : round(discount_applied, 2),
        'platform_fee' : platform_fee,
        'delivery_charges' : round(delivery_charges, 2),
        'grand_total' : round(grand_total, 2)
    }

    return render(request, 'Pharmacy/pharmacy_cart.html', context)