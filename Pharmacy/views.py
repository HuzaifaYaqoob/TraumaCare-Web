from django.shortcuts import render
from Product.models import Product
# Create your views here.

def PharmacyLandingPage(request):
    context = {}
    medicines = Product.objects.filter(is_active=True, is_deleted=False, is_blocked=False)[:10]


    context['medicines'] = medicines
    return render(request, 'Pharmacy/pharmacy_landing.html', context)

def PharmacySearchPage(request):
    return render(request, 'Pharmacy/pharmacy_search.html')

def PharmacyCartPage(request):
    return render(request, 'Pharmacy/pharmacy_cart.html')