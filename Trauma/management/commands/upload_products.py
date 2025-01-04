from django.core.management.base import BaseCommand
from Product.models import Product, ProductCategory, SubCategory, ProductForm, ProductType, TreatmentType
from Pharmacy.models import Store, StoreLocation
from Vendor.models import Vendor
from Pharmaceutical.models import Pharmaceutical
import json


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):


        first_store = Store.objects.filter(name='TraumaCare MediMart')[0]

        with open('Files/Medicine/dvago_medicines.json', 'r') as input_file:
            reader = json.load(input_file)
            for row_i, row in enumerate(reader):
                
                vendor = None
                manufacturer = None
                treatment_type = None
                product_form = None
                product_type = None

                if row.get('Brand'):
                    vendor = Vendor.objects.get_or_create(name=row['Brand'])[0]
                
                if row.get('Brand'):
                    manufacturer = Pharmaceutical.objects.get_or_create(name=row['Brand'])[0]
                
                if row.get('Usedfor'):
                    treatment_type = TreatmentType.objects.get_or_create(name=row['Usedfor'])[0]
                
                if row.get('Variations'):
                    product_form = ProductForm.objects.get_or_create(name=row['Variations'])[0]
                
                if row.get('Variations'):
                    product_type = ProductType.objects.get_or_create(name=row['Variations'])[0]
                    
                price = float(row['Price'])
                discount_price = float(row['DiscountPrice'])
                discount_percentage = 100 - ((discount_price / price) * 100)
                
                prod = Product.objects.create(
                    store = first_store,
                    Vendor = vendor,
                    manufacturer = manufacturer,
                    treatment_type = treatment_type,
                    product_form = product_form,
                    product_type = product_type,
                    name = row['Title'],
                    description = row['Description'],
                    price = price,
                    discount = round(discount_percentage, 2),
                    max_order = row.get('MaxOrder', 100) or 100,
                    # generic_category = row['Generic Category'],
                    # formulation = row['Ingredients'],
                    # strength = row['Strength'],
                    pack_size = f"{row.get('NoofStrips')} {row.get('Variations')}",
                    prescription_required = True if row['PrescriptionRequired'] == 'True' else False,
                    pack_form = f"{row.get('NoofStrips')} {row.get('Variations')}",
                    key_highlights = row.get('Highlights', ''),
                    # storage = row['Storage'],
                    # habit_forming = row['Habit Forming'],
                    # sedation = row['Sedation'],
                    # child_safety = row['Child Safety'],
                    # marketed_by = row['Marketed By'],
                    # route_of_administration = row['Route of Administration'],
                    Images = row.get('ProductImage', ''),
                )
                subcategories = row.get('SubCategory', None)
                if not subcategories:
                    main_cat = row.get('Category', None) or row.get('CategoryName', None)
                    if main_cat:
                        subcategories = SubCategory.objects.filter(category__name=main_cat)
                        for cat_obj in subcategories:
                            prod.sub_category.add(cat_obj)
                else:
                    subcategories = subcategories.split(',')
                    if 'Medicine' in subcategories:
                        subcategories.remove('Medicine')
                    if 'Non Medicine' in subcategories:
                        subcategories.remove('Non Medicine')
                    for cat in subcategories:
                        try:
                            cat_obj = SubCategory.objects.get(name=cat)
                        except Exception as err:
                            print(err)
                            print(f'Category Name : {cat}')
                        else:
                            prod.sub_category.add(cat_obj)
                
                print(f'Product Added : {row_i} : {prod.sub_category.count()} {prod.name}')
        self.stdout.write(self.style.SUCCESS('Product Uploaded Successfully'))

