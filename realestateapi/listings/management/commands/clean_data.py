# listings/management/commands/clean_data.py
from django.core.management.base import BaseCommand
from listings.utils import clean_data

class Command(BaseCommand):
    help = 'Clean scrapped data from database'
    def handle(self, *args, **options):
        try:
           clean_data()
        except Exception as e:
           self.stdout.write(self.style.ERROR(f"ERROR in cleaning the data,{e}"))
           return
        
        self.stdout.write(self.style.SUCCESS('Clean data management command executed successfully'))

