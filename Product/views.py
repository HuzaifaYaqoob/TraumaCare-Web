from django.shortcuts import render

# Create your views here.


def productDetailPage(request):
    return render(request, 'Product/product_details.html')