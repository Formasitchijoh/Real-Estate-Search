# listings/management/commands/load_data.py
from django.core.management.base import BaseCommand
from listings.utils import Scrapper

class Command(BaseCommand):
    help = 'Load processed data from CSV file'

    def handle(self, *args, **options):
        try:
             Scrapper()
        except Exception as e:
             self.stdout.write(self.style.ERROR(f"ERROR in loading scrapped data {e}"))
             return
    
        self.stdout.write(self.style.SUCCESS('scrape command executed successfully'))