

from django.shortcuts import render


def homePage(request):
    return render(request, 'Home/index.html')