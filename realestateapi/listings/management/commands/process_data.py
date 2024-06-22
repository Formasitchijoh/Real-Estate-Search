# listings/management/commands/clean_data.py
from django.core.management.base import BaseCommand
from listings.utils import match_listings_to_query, match_query_to_listings, generate_queries,load_processed_data

class Command(BaseCommand):
    help = 'process cleaned data from csv file'

    def handle(self, *args, **options):
        try:
            match_listings_to_query()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in match_listing_to_queries():{e}"))
            return
        try:
            generate_queries()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in the generate queries():{e}"))
            return
        try:
            match_query_to_listings()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in matching query to listings():{e}"))
            return
        try:
            load_processed_data()
        except Exception as e :
            self.stdout.write(self.style.ERROR(f"ERROR in loading processed data into  the database:{e}"))
            return
        self.stdout.write(self.style.SUCCESS('process command executed successfully'))