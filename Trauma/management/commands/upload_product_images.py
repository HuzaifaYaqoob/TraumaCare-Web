



from django.core.management.base import BaseCommand

from Product.models import Product, ProductImage

import requests
from django.core.files.base import ContentFile

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):

        products = Product.objects.exclude(Images='')

        for pi, product in enumerate(products):
            print(f'{pi} / {len(products)}')
            # fetch Image from url and save in product image 
            for url in product.Images.split(','):
                url = url.split('?')[0]
                url = url.split('//ailaaj.pk')[-1]
                url = f'https://ailaaj.pk{url}'


                response = requests.get(url)
                if response.status_code == 200:
                    file_name = url.split("/")[-1]
                    
                    # Create a ProductImage instance
                    product_image = ProductImage.objects.create(product=product)
                    
                    # Save the downloaded image to the ProductImage instance
                    product_image.image.save(file_name, ContentFile(response.content), save=True)

                    print(f"ProductImage created with ID: {product_image.id}")
                    
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")
                
            print(product)
            product.Images = ''
            product.save()


        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

