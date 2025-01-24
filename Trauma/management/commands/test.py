



from django.core.management.base import BaseCommand

import csv
from django.conf import settings
from datetime import datetime
import time
import re
import random

from Product.models import Product, ProductStock
from Pharmacy.models import Store, StoreLocation

from Authentication.models import User

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        products = Product.objects.all()
        for index, product in enumerate(products):
            print(f'{index} / {len(products)}')
            stocks = ProductStock.objects.filter(product=product).order_by('-price')
            print(stocks[0].price)
            print(stocks[1].price)
            stocks.update(price=stocks[0].price)


        self.stdout.write(self.style.SUCCESS('Successfully added'))