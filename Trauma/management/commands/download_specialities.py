


from django.core.management.base import BaseCommand

from Constants.AddDataToDB import download_all_specialities

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        download_all_specialities()
        self.stdout.write(self.style.SUCCESS('Successfully Downloaded Specialities'))