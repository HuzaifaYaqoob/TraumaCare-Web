from django.shortcuts import render, redirect
from django.db.models import Q
from Product.models import Product, ProductStock, SubCategory, TreatmentType, ProductForm, ProductType
from Pharmaceutical.models import Pharmaceutical
from Profile.models import ShipingAddress
from Order.models import Order, OrderItem

import json
from urllib.parse import unquote
from django.contrib import messages
from Constants.Emails.OrderEmail import sendNewOrderEmailToAdmin
# Create your views here.

def PharmacyLandingPage(request):
    context = {}
    medicines = Product.objects.filter(
        is_active=True, 
        is_deleted=False, 
        is_blocked=False
    ).select_related('store').prefetch_related(
        'product_images',
        'product_stocks',
        'product_stocks__location',
    ).order_by('?')[:10]

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


    context['product_TreatmentTypes'] = TreatmentType.objects.filter(is_active=True).order_by('name')[:20]
    context['product_product_forms'] = ProductType.objects.filter(is_active=True).order_by('name')[:20]
    context['product_subcategories'] = SubCategory.objects.filter(is_active=True).order_by('name')[:20]
    context['brands'] = Pharmaceutical.objects.filter(is_active=True, is_deleted=False).order_by('name')[:20]
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
            product = Product.objects.get(id = item['id'])
            stock = ProductStock.custom_objects.filter(product = product, location__id = item['location_stock'], is_active=True, is_deleted=False).order_by('-created_at').first()
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

    similar_query = {}
    if len(categories) > 0:
        similar_query['sub_category__name__in'] = categories
    similar_products = Product.objects.filter(
        is_active=True, is_deleted=False, is_blocked=False,
        **similar_query
    ).distinct().exclude(id__in=[item.get('id') for item in CartItems]).order_by('?')[:10]

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

def PharmacyCartCheckoutPage(request):
    cookie_data = request.COOKIES.get('CartItems', '')

    if cookie_data:
        decoded_data = unquote(cookie_data)
        CartItems = json.loads(decoded_data)
    else:
        CartItems = []
    products = []
    categories = []
    subtotal = 0
    discount_applied = 0
    platform_fee = 9
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

            
            categories.extend(list(product.sub_category.all().values_list('name', flat=True).distinct()))
            quantity = int(item['quantity'])
            images = product.product_all_images
            image = None
            if len(images) > 0 and images[0].image:
                image = images[0].image.url
            
            subtotal += stock.final_price * quantity
            if stock.discount:
                discount_applied += (stock.price - stock.final_price) * quantity
            
            p_price = stock.final_price
            p_discount = stock.price - stock.final_price
            
            products.append([product, stock, quantity, p_price, p_discount])

    grand_total = (subtotal - discount_applied) + platform_fee + delivery_charges
    similar_products = []
    if request.method == 'POST':
        selected_shipping_address = request.POST.get('selected_shipping_address', None)
        if selected_shipping_address:
            shipping_address = ShipingAddress.objects.get(id = selected_shipping_address)
        else:
            shipping_name = request.POST.get('shipping_name', None)
            shipping_phone = request.POST.get('shipping_phone', None)
            shipping_address = request.POST.get('shipping_address', None)

            shipping_address = ShipingAddress.objects.create(
                user = request.user,
                full_name = shipping_name,
                address = shipping_address,
                mobile_number = shipping_phone
            )

        order = Order.objects.create(
            user = request.user,
            shipping = shipping_address,
            subtotal = subtotal,
            discount = discount_applied,
            platform_fee = platform_fee,
            delivery_charges = delivery_charges,
            total_amount = grand_total,
            payment_method = 'COD',
            payment_status = 'PENDING',
        )

        for p in products:
            OrderItem.objects.create(
                order = order,
                product = p[0],
                stock = p[1],
                quantity = p[2],
                price = p[3],
                discount = p[4],
                final_price = p[3] - p[4],
            )
        
        try:
            sendNewOrderEmailToAdmin(order)
        except:
            pass
        
        messages.success(request, 'Order Placed Successfully')
        return redirect('CheckoutSuccessPage', order_id=order.id)

    else:
        similar_query = {}
        if len(categories) > 0:
            similar_query['sub_category__name__in'] = categories
        similar_products = Product.objects.filter(
            is_active=True, is_deleted=False, is_blocked=False,
            **similar_query
        ).distinct().exclude(id__in=[item.get('id') for item in CartItems]).order_by('?')[:10]

    

    user_shipping_addresses = ShipingAddress.objects.filter(user = request.user, is_deleted=False).order_by('-created_at')
    context = {
        'user_shipping_addresses' : user_shipping_addresses,
        'similar_products' : similar_products,
        'subtotal' : round(subtotal, 2),
        'discount_applied' : round(discount_applied, 2),
        'platform_fee' : platform_fee,
        'delivery_charges' : round(delivery_charges, 2),
        'grand_total' : round(grand_total, 2)
    }

    return render(request, 'Pharmacy/pharmacy_checkout.html', context)


def CheckoutSuccessPage(request, order_id):
    try:
        order = Order.objects.get(id = order_id)
    except Exception as err:
        messages.error(request, 'Invalid Order Id')
        return redirect('PharmacyLandingPage')
    response = render(request, 'Pharmacy/pharmacy_checkout_success.html')
    response.delete_cookie('CartItems')
    return response