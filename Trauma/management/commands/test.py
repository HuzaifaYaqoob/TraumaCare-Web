



from django.core.management.base import BaseCommand

import csv

from Blog.Cronjob import generateBlogPost
from Blog.models import BlogPostTopic, BlogMedia
from django.conf import settings
from PIL import Image

from datetime import datetime
import time


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        mm = BlogMedia.objects.filter()
        for m in mm:
            if not m.thumbnail:
                if '.webp' in m.image.name:
                    continue
                ext = m.image.name.split('.')[-1]
                url = f'{settings.BASE_DIR}{m.image.url}'.replace('%3A', ':')
                try:
                    background = Image.open(url)
                except Exception as err:
                    print(err)
                    continue
                bg_w, bg_h = background.size
                print(url)

                time.sleep(1)
                time_now = datetime.now()

                slug = m.post.slug
                slug = slug.replace(' ', '-').replace('/', '-').replace(':', '-').replace('--', '-')
                new_width = 400
                if bg_w > new_width:
                    bg_h = int((new_width / bg_w) * bg_h)
                    bg_w = new_width

                    background = background.resize((bg_w, bg_h), Image.ANTIALIAS)

                saving_url = f"media/Blog/Images/traumacare-{slug[0:30]}-{time_now.strftime("%d-%H%M%S")}-{bg_w}X{bg_h}.{ext}"
                background.save(saving_url, quality=95)
                m.thumbnail = f'{saving_url}'.split('media/')[-1]
                m.save()

        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

