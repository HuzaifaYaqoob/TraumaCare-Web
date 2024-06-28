from django.shortcuts import render

from Blog.models import BlogPost

# Create your views here.


def BlogHomePage(request):
    context = {
        'posts' : BlogPost.objects.all().order_by('-created_at')[:20]
    }
    return render(request, 'Blog/blog-home.html', context)