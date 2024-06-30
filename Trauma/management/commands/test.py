



from django.core.management.base import BaseCommand

import csv

from Blog.Cronjob import generateBlogPost
from Blog.models import BlogPostTopic, BlogMedia

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        mm = BlogMedia.objects.filter(is_thumbnail_generated=False)
        for m in mm:
            print(m.image.url)
            m.save()

        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

