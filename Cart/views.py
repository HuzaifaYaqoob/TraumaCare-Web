from django.shortcuts import render

# Create your views here.


def CartPage(request):
    return render(request, 'Cart/Cart.html')