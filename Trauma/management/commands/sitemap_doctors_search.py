



from django.core.management.base import BaseCommand
from Product.generate_sitemap import registerSearchPageDoctorsSiteMaps

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        registerSearchPageDoctorsSiteMaps()

        self.stdout.write(self.style.SUCCESS('Successfully added'))