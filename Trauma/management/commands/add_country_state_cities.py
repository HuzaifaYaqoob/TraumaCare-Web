


from django.core.management.base import BaseCommand

from Constants.AddDataToDB import add_country_state_cities

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        add_country_state_cities()
        self.stdout.write(self.style.SUCCESS('Successfully added Country States Cities'))