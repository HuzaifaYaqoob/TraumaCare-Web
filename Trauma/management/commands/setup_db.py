



from django.core.management.base import BaseCommand

from Constants.AddDataToDB import add_country_state_cities
from Constants.AddDataToDB import add_diseases
from Constants.AddDataToDB import add_specialities




class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        add_diseases()
        add_specialities()
        add_country_state_cities()
    
        self.stdout.write(self.style.SUCCESS('Successfully Setuped DB'))

