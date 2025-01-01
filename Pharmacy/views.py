from django.shortcuts import render

# Create your views here.


def PharmacySearchPage(request):
    return render(request, 'Pharmacy/pharmacy_search.html')