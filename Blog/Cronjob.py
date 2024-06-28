


from .models import BlogMedia, BlogPost, Category, Tag


from Secure.models import XpoKey
from ChatXpo.Sockets.Constant.Query import askChatXpo


posts_data = [
    'What Causes Skin Tags? And How to Remove Them',
    'Amazing Benefits Of Applying Ice On Your Face!',
    'Skincare For Men: Overview and Products To Use',
    'Acne and Acne Scars',
    'Home Remedies To Get Rid Of Dark Knuckles Fast!',
    'How To Whiten Skin Overnight Naturally',
    'Surgical Methods Of Face Rejuvenation',
    '10 Benefits Of Vitamin E Capsules For Hair And Skin',
    'What To Avoid When Taking Glutathione?',
    'How To Get Dimples Permanently Without Surgery',
    'How To Reduce Lip Size Naturally Without Surgery',
    'Is Vaseline Good For Your Face?',
    'Biotin: Benefits, Side Effects & More',
    '13 Amazing Benefits Of Shea Butter',
    'Hair Loss in Females: Causes, Treatment, and Prevention',
    'Common Causes Of Acne And How You Can Avoid Them',
    'Top 10 Reasons For Hair Fall And Its Remedies',
    'How To Cure Shingles In 3 Days – Is It Possible?',
    'How To Get Rid Of Bags Under Eyes',
    'Sciatica Pain in Women: Causes, Symptoms, and Management',
    'Knee Pain in Women: Causes, Symptoms, and Treatments',
    'Osteoarthritis: Causes, Symptoms, Diagnosis & Treatment',
    'Arthritis Of Joints – Symptoms, Types & Treatment',
    'Tennis Elbow – Causes, Symptoms & Treatment',
    'Dorsalgia: Types, Causes, Symptoms & Treatment',
    '5 Great Tips for a Healthy Spine',
    '4 Most Common Childhood Orthopedic Conditions',
    '5 Ways to Manage Bad Days With Rheumatoid Arthritis',
    '5 Best Tips for Exercising With Osteoarthritis',
    'Vitamin D Deficiency Makes Bones Age Faster, Research Finds',
    'Dorsalgia: Types, Causes, Symptoms & Treatment',
    'Warning Signs of Breast Cancer – Breast Cancer Awareness Month 2024',
    '10 Early Symptoms Of Lung Cancer – Lung Cancer Awareness Month 2024',
    'Exploring Bladder Cancer Treatments',
    '9 Subtle Signs Of Cancer You Shouldn’t Ignore',
    'Period Essentials: Dos & Don’ts You Should Know About',
    'Skincare For Men: Overview and Products To Use',
    '7 Amazing Benefits Of Applying Ice On Your Face!',
    'Hormonal Contraception: It’s Type and Usage',
    'Why Should You Not Use Vagina Whitening Creams?',
]

def generateBlogPost():
    key = XpoKey.objects.filter(is_deleted = False, is_active=True).order_by('-total_requests')[0]


    data = []
    
    # posts = BlogPost.objects.all()
    # if posts.count() == 0:
        # data.append({
        #     'role' : 'system',
        #     'content' : f'Following are the existing posts, and categories available on Traumacare.',
        # })
        # for post in posts:
        #     data.append({
        #         'role' : 'system',
        #         'content' : f'Post : {post.title}, Category : {post.category.name}',
        #     })
    data.append({
        'role' : 'system',
        'content' : f'You are an AI Autobloger Bot that automatically generate Blog post for healthcare application. Traumacare is a healthcare application. Generate blog posts',
    })
    # data.append({
    #     'role' : 'system',
    #     'content' : f'Most IMPORTANT ::: also generate post on Diseases which are most actively affecting our patients. We are trying to increase our traffic',
    # })
    data.append({
        'role' : 'system',
        'content' : f'Most IMPORTANT ::: Blog Post content must be greater than 5000 words. Post must be too lengthy',
    })
    data.append({
        'role' : 'system',
        'content' : f'Make Title more efficient and realistic',
    })

    for p in posts_data:
        response = askChatXpo(
            f'Write an article on {p}, Title must be in simple words, so everyone can understand easily',
            previousQueries=data,
            # instructions=False,
            user=None,
            inputFunction='generate_blog_post'
        )
        break

    print(response)
    