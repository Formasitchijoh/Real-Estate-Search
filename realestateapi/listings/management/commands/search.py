# listings/management/commands/load_data.py
from django.core.management.base import BaseCommand
from listings.utils import similarity_check

class Command(BaseCommand):
    help = 'process similarity result'

    def handle(self, *args, **options):
        try:
              similarity_check()
        except Exception as e :
            self.stdout.write(self.style.ERROR(f"ERROR in searching listings:{e}"))
            return
    
        self.stdout.write(self.style.SUCCESS(' results returned  successfully'))