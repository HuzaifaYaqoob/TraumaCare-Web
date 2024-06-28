from django.shortcuts import render

from Blog.models import BlogPost

from django.db.models import Count
# Create your views here.


def BlogHomePage(request):
    context = {
        'posts' : BlogPost.objects.annotate(media = Count('media')).filter(media__gt = 0).order_by('-created_at')[:20]
    }
    return render(request, 'Blog/blog-home.html', context)