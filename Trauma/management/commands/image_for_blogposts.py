



from django.core.management.base import BaseCommand

import csv

from Blog.Cronjob import generateBlogPost
from Blog.models import BlogPostTopic, BlogMedia, BlogPost
from django.conf import settings
from PIL import Image
from django.db.models import Count

from datetime import datetime
import time
import requests
import os
from ChatXpo.Constants.AI import GenerateImage

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        posts = BlogPost.objects.annotate(count=Count('blog_post_medias')).filter(count=0)
        for index, post in enumerate(posts):

            prompt = f'Generate an image where title is {post.title}, category is {post.category.name} and Description is {post.content_content[:100]}, You may include setting with advanced medical equipment and technology if necessary. You may Include if necessary elements like holographic displays, robotic assistants, and innovative medical devices to depict a cutting-edge healthcare environment. Use the primary color #0A1C4B for the main elements and the secondary color #24D0D0 for accents and highlights to enhance the visual appeal.'
            print('*'*50)
            print(f'{index}/{len(posts)}')
            print(post)
            image_url = GenerateImage(prompt, size='1792x1024', quality='standard')

            print(image_url)

            url = image_url

            time_now = datetime.now()
            
            img_data = requests.get(url).content
            path = f'{settings.BASE_DIR}/media/{post.slug}-{time_now.strftime("%d-%H%M%S")}-1792x1024.jpg'
            print(path)
            with open(path, 'wb') as handler:
                handler.write(img_data)

            BlogMedia.objects.create(
                post = post,
                image = path
            )

            os.remove(path)

        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))


