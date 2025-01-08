from django.shortcuts import render
from django.db.models import Q
from Product.models import Product
# Create your views here.

def PharmacyLandingPage(request):
    context = {}
    medicines = Product.objects.filter(is_active=True, is_deleted=False, is_blocked=False).order_by('?')[:10]


    context['medicines'] = medicines
    return render(request, 'Pharmacy/pharmacy_landing.html', context)

def PharmacySearchPage(request):
    context = {}
    searchQuery = request.GET.get('searchQuery', '')

    searchedProducts = Product.objects.filter(
        Q(name__icontains = searchQuery),
        is_active=True, is_deleted=False, is_blocked=False,
    )

    context['medicines'] = searchedProducts[:28]
    return render(request, 'Pharmacy/pharmacy_search.html', context)

def PharmacyCartPage(request):
    return render(request, 'Pharmacy/pharmacy_cart.html')