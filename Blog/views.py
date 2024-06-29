from django.shortcuts import render, redirect

from Blog.models import BlogPost

from django.db.models import Count
# Create your views here.


def BlogHomePage(request):
    context = {
        'posts' : BlogPost.objects.annotate(media = Count('blog_post_medias')).filter(media__gt = 0).order_by('-created_at')[:20]
    }
    return render(request, 'Blog/blog-home.html', context)

def PostViewPage(request, post_slug):
    try:
        post = BlogPost.objects.get(slug = post_slug)
    except:
        return redirect('BlogHomePage')

    context = {
        'post' : post
    }
    return render(request, 'Blog/blog-post.html', context)