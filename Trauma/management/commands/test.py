



from django.core.management.base import BaseCommand

import csv
from django.conf import settings
from datetime import datetime
import time
import re

import geopy.distance

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        my_coords = (31.48457979046869, 74.26311376936425)
        hospital_coords = (31.47969739187253, 74.2803748868337)

        print(geopy.distance.geodesic(my_coords, hospital_coords).km)


        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

