



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

        users = User.objects.all()
        for u in users:
            if u.first_name:
                u.full_name = f'{u.first_name} {u.last_name if u.last_name else ""}'
            else :
                u.full_name = u.username
            u.save()
            

        self.stdout.write(self.style.SUCCESS('Successfully added'))