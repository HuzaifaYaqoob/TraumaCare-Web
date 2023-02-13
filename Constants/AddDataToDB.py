

import json

from Trauma.models import Speciality

def add_specialities():

    with open('Files/Specialities.json' , 'r') as input_file:
        input_file = json.load(input_file)
        for row in input_file:
            spec, created = Speciality.objects.get_or_create(name = row['name'])
            spec.svg_icon = row['svg_icon']
            spec.color_code = row['color']
            spec.save()