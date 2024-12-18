

import json
import csv
from Trauma.models import Speciality, Country, State, City, Disease

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

def add_diseases():

    with open('Files/Diseases.json' , 'r') as input_file:
        input_file = json.load(input_file)
        for row in input_file:
            disease, created = Disease.objects.get_or_create(name = row['name'])
            disease.svg_icon = row['svg_icon']
            disease.color_code = row['color_code']
            disease.description = row['description']
            disease.image = row['image']
            disease.rank = row['rank']
            disease.save()


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


def download_all_diseases():
    with open('Files/Diseases.json' , 'w') as input_file:
        diseases = Disease.objects.all()
        data = []

        for disease in diseases:
            svg_icon = str(disease.svg_icon)
            svg_icon = svg_icon.replace('"', "'")
            for i in [11, 12, 13, 14, 15, 16 ,17, 18, 19]:
                svg_icon = svg_icon.replace(f"width='{i}'", '')
                svg_icon = svg_icon.replace(f"height='{i}'", '')

            data.append({
                'name' : str(disease.name),
                'svg_icon' : svg_icon,
                'color_code' : str(disease.color_code),
                'description' : str(disease.description),
                'image' : str(disease.image),
                'rank' : disease.rank,
            })
        
        data = json.dump(data, input_file)


def add_country_state_cities():
    with open('Files/Countries.json', 'r') as country_file:
        countries = json.load(country_file)
        for country in countries:
            country_name = country['country_name']
            svg_icon = country['svg_icon']
            unique_code = country['unique_code']
            country_code = country['country_code']
            dial_code = country['dial_code']

            this_country, creatd = Country.objects.get_or_create(
                name = country_name,
                dial_code = dial_code
            )
            
            this_country.color_code = country_code
            this_country.svg_icon = svg_icon
            # this_country.description
            # this_country.flag
            this_country.save()

            with open('Files/states.csv', 'r') as state_file:
                states = csv.reader(state_file)
                for state in states:
                    country_unique_id = state[2]
                    if country_unique_id == unique_code:
                        state_name = state[1]
                        state_code = state[0]
                        this_state, created = State.objects.get_or_create(
                            name = state_name,
                            country = this_country
                        )
                        with open('Files/cities.csv', 'r') as city_file:
                            cities = csv.reader(city_file)
                            for city in cities:
                                state_unique_id = city[2]
                                if state_unique_id == state_code:
                                    city_name = city[1]
                                    City.objects.get_or_create(
                                        name = city_name,
                                        country = this_country, 
                                        state = this_state
                                    )