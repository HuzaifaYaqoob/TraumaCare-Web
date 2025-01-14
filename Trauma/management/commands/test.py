



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

        self.stdout.write(self.style.SUCCESS('Successfully added'))