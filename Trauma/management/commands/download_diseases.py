


from django.core.management.base import BaseCommand

from Constants.AddDataToDB import download_all_diseases

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        download_all_diseases()
        self.stdout.write(self.style.SUCCESS('Successfully Downloaded Diseases'))