



from django.core.management.base import BaseCommand

import csv

from Blog.Cronjob import generateBlogPost

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        generateBlogPost()
        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

