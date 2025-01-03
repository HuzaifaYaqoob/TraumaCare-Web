



from django.core.management.base import BaseCommand

import csv

from Product.models import Product, ProductCategory, SubCategory, ProductForm, ProductType, TreatmentType
from Pharmacy.models import Store, StoreLocation
from Vendor.models import Vendor
from Pharmaceutical.models import Pharmaceutical

import time


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        prods = Product.objects.all()
        for pi, prod in enumerate(prods):
            old_price = prod.price
            if old_price > 120:
                fixed_percentage = 10
            else:
                fixed_percentage = 30

            new_price = round(old_price * (1 + fixed_percentage / 100), 2)

            print(f"{pi} : {prod.name}: Old Price = {old_price}, New Price = {new_price}")
            prod.price = new_price
            prod.save()

        self.stdout.write(self.style.SUCCESS('Product Uploaded Successfully'))

