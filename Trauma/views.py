

from django.shortcuts import render


def homePage(request):
    return render(request, 'Home/index.html')


def test_huzaifa(request):
    return render(request, 'Huzaifa/test.html')
