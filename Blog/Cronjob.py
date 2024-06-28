


from .models import BlogMedia, BlogPost, Category, Tag


from Secure.models import XpoKey
from ChatXpo.Sockets.Constant.Query import askChatXpo

def generateBlogPost():
    key = XpoKey.objects.filter(is_deleted = False, is_active=True).order_by('-total_requests')[0]


    data = []
    
    posts = BlogPost.objects.all()
    if posts.count() == 0:
        data.append({
            'role' : 'system',
            'content' : f'Following are the existing posts, and categories available on Traumacare.',
        })
        for post in posts:
            data.append({
                'role' : 'system',
                'content' : f'Post : {post.title}, Category : {post.category.name}',
            })
    data.append({
        'role' : 'system',
        'content' : f'You are an AI Autobloger Bot that automatically generate Blog post for healthcare application. Traumacare is a healthcare application. Generate blog posts',
    })
    data.append({
        'role' : 'system',
        'content' : f'Most IMPORTANT ::: also generate post on Diseases which are most actively affecting our patients. We are trying to increase our traffic',
    })
    response = askChatXpo(
        'Generate a blog post for above instructions. Generate Title, Content, Tags, Read time, category. C',
        previousQueries=data,
        # instructions=False,
        user=None,
        inputFunction='generate_blog_post'
    )

    print(response)
    