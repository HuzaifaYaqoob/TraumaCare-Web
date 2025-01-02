



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
        first_store = Store.objects.all()[0]
        with open('Files/Medicine/products.csv', 'r') as input_file:
            reader = csv.DictReader(input_file)
            for row_i, row in enumerate(list(reader)):
                vendor = None
                manufacturer = None
                treatment_type = None
                product_form = None
                product_type = None

                if row['Vendor']:
                    vendor = Vendor.objects.get_or_create(name=row['Vendor'])[0]
                
                if row['Manufacturer']:
                    manufacturer = Pharmaceutical.objects.get_or_create(name=row['Manufacturer'])[0]
                
                if row['CardIngredients']:
                    treatment_type = TreatmentType.objects.get_or_create(name=row['CardIngredients'])[0]
                
                if row['Product Form']:
                    product_form = ProductForm.objects.get_or_create(name=row['Product Form'])[0]
                
                if row['Product Type']:
                    product_type = ProductType.objects.get_or_create(name=row['Product Type'])[0]
                    
                price = row['OriginalPrice'].replace('Rs.', '').replace(',', '').replace(' ', '')
                
                prod = Product.objects.create(
                    store = first_store,
                    Vendor = vendor,
                    manufacturer = manufacturer,
                    treatment_type = treatment_type,
                    product_form = product_form,
                    product_type = product_type,

                    name = row['Name'],
                    description = row['Name'],
                    price = price,
                    generic_category = row['Generic Category'],
                    formulation = row['Ingredients'],
                    strength = row['Strength'],
                    pack_size = row['Pack Size'],
                    prescription_required = True if row['CardPrescriptionRequired'] == 'Yes' else False,
                    pack_form = row['Pack Form'],
                    key_highlights = row['Key Highlights'],
                    storage = row['Storage'],
                    habit_forming = row['Habit Forming'],
                    sedation = row['Sedation'],
                    child_safety = row['Child Safety'],
                    marketed_by = row['Marketed By'],
                    route_of_administration = row['Route of Administration'],
                    Images = row['Images'],
                )
                categories = row['Categories'].split(',')
                if 'Medicine' in categories:
                    categories.remove('Medicine')
                if 'Non Medicine' in categories:
                    categories.remove('Non Medicine')

                for cat in categories:
                    try:
                        cat_obj = SubCategory.objects.get(name=cat)
                    except Exception as err:
                        print(err)
                        print(f'Category Name : {cat}')
                    else:
                        prod.sub_category.add(cat_obj)
                
                print(f'Product Added : {row_i} : {prod.name}')

                # sub_category = 

        self.stdout.write(self.style.SUCCESS('Product Uploaded Successfully'))

