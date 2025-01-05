from django.shortcuts import render

# Create your views here.

def PharmacyLandingPage(request):
    return render(request, 'Pharmacy/pharmacy_landing.html')

def PharmacySearchPage(request):
    return render(request, 'Pharmacy/pharmacy_search.html')

def PharmacyCartPage(request):
    return render(request, 'Pharmacy/pharmacy_search.html')