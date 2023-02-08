from django.shortcuts import render

# Create your views here.



def LoginPage(request):
    return render(request, 'Auth/login.html')


def RegisterPage(request):
    return render(request, 'Auth/joinpage2.html')