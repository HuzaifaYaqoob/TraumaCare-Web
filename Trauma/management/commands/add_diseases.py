


from django.core.management.base import BaseCommand

from Constants.AddDataToDB import add_diseases

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        add_diseases()
        self.stdout.write(self.style.SUCCESS('Successfully added Diseases'))