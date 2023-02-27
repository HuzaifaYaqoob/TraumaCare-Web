



from django.core.management.base import BaseCommand

import csv

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        with open('Files/cities.csv', 'r') as input_file:
            rows = csv.reader(input_file)
            states_ids = []
                
            with open('Files/states.csv', 'r') as state_files:
                    state_reader = csv.reader(state_files)
                    print(state_reader)
                    for st in state_reader:
                        states_ids.append(st[0])
            
            states_ids = set(states_ids)
            states_ids = list(states_ids)
            new_rows = []
            for row in rows:
                st_id = row[2]
                if st_id in states_ids:
                    new_rows.append(row)
            print(new_rows)
            with open('Files/cities.csv', 'w') as write_file:
                writer = csv.writer(write_file)
                writer.writerows(new_rows)

    
        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

