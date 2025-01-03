



from django.core.management.base import BaseCommand

import csv

from Product.models import Product, ProductCategory, SubCategory, ProductForm, ProductType, TreatmentType
from Pharmacy.models import Store, StoreLocation
from Vendor.models import Vendor
from Pharmaceutical.models import Pharmaceutical

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        with open('Files/Medicine/products.csv', 'r') as input_file:
            reader = csv.DictReader(input_file)
            for row_i, row in enumerate(list(reader)):
                price = row['OriginalPrice'].replace('Rs.', '').replace(',', '').replace(' ', '')
                DiscountedPrice = row['DiscountedPrice'].replace('Rs.', '').replace(',', '').replace(' ', '')
                if not DiscountedPrice:
                    continue
                percentage = 100 - ((float(DiscountedPrice) / float(price)) * 100)
                
                try:
                    prod = Product.objects.get(name = row['Name'])
                except Exception as err:
                    print('*' * 50)
                    print(row['Name'])
                    print(err)
                    print('*' * 50)
                else:
                    prod.discount = round(percentage, 2)
                    prod.save()
                    print(f'Saved {prod.price} : {prod.discount}')
                

                # sub_category = 

        self.stdout.write(self.style.SUCCESS('Product Uploaded Successfully'))

