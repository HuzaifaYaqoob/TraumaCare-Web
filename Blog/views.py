from django.shortcuts import render

# Create your views here.


def BlogHomePage(request):
    return render(request, 'Blog/blog-home.html')