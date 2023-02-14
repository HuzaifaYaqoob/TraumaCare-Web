

import json

from Trauma.models import Speciality

def add_specialities():

    with open('Files/Specialities.json' , 'r') as input_file:
        input_file = json.load(input_file)
        for row in input_file:
            spec, created = Speciality.objects.get_or_create(name = row['name'])
            spec.svg_icon = row['svg_icon']
            spec.color_code = row['color_code']
            spec.description = row['description']
            spec.image = row['image']
            spec.rank = row['rank']
            spec.save()


def download_all_specialities():
    with open('Files/Specialities.json' , 'w') as input_file:
        specs = Speciality.objects.all()
        data = []

        for sp in specs:
            svg_icon = str(sp.svg_icon)
            svg_icon = svg_icon.replace('"', "'")
            for i in [11, 12, 13, 14, 15, 16 ,17, 18, 19]:
                svg_icon = svg_icon.replace(f"width='{i}'", '')
                svg_icon = svg_icon.replace(f"height='{i}'", '')

            data.append({
                'name' : str(sp.name),
                'svg_icon' : svg_icon,
                'color_code' : str(sp.color_code),
                'description' : str(sp.description),
                'image' : str(sp.image),
                'rank' : sp.rank,
            })
        
        data = json.dump(data, input_file)