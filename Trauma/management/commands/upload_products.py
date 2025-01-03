



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
            pass

        self.stdout.write(self.style.SUCCESS('Product Uploaded Successfully'))

