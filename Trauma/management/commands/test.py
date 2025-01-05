



from django.core.management.base import BaseCommand

import csv
from django.conf import settings
from datetime import datetime
import time
import re
import random

from Product.models import Product, ProductStock
from Pharmacy.models import Store, StoreLocation

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):

        for store in Store.objects.all():
            store_locations = store.store_locations.all()
            products = Product.objects.filter(store=store)

            for product in products:
                price = product.price
                discount = product.discount
                
                for location in store_locations:
                    should_increase = random.choice([True, False])
                    increment = random.randint(1, 10)
                    sold = random.randint(1, 100)

                    new_price = price

                    if should_increase:
                        new_price += increment
                    else:
                        new_price -= increment

                    prod_stock, created = ProductStock.objects.get_or_create(
                        product = product,
                        location = location,
                    )
                    prod_stock.quantity = 10000
                    prod_stock.sold = sold
                    prod_stock.price = new_price
                    prod_stock.discount = discount
                    prod_stock.save()
                
                print(product.name)


        self.stdout.write(self.style.SUCCESS('Successfully added'))