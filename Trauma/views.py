

from django.shortcuts import render


def homePage(request):
    return render(request, 'Home/index.html')


def FeedPage(request):
    return render(request, 'Feed/feedPage.html')

def test(request):
    return render(request, 'prescription.html')

def CartPage(request):
    return render(request, 'User/cart.html')

def searchFilterPage(request):
    # return render(request, 'Search/booklabtest.html')
    return render(request, 'Search/Updated_FilterPage.html')

