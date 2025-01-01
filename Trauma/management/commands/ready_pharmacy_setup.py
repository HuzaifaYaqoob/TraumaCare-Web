



from django.core.management.base import BaseCommand

import csv


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        with open('Files/store_product_categories.csv' , 'r') as input_file:
            pass

        self.stdout.write(self.style.SUCCESS('Categories & Subcategories Added'))

