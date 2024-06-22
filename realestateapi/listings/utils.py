import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import csv
# realestateapi/listings/utils.py
from .models import ProcessedListings
with open('processed_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ProcessedListings.objects.create(
            query=row['query'],
            Unnamed=row['Unnamed'],
            title=row['title'],
            image=row['image'],
            link=row['link'],
            listing_type=row['listing_type'],
            bedroom=row['bedroom'],
            bathrooms=row['bathrooms'],
            location=row['location'],
            town=row['town'],
            price=row['price'],
            pricepermonth=row['pricepermonth'],
            views=row['views'],
            reactions=row['reactions']
            # ... other fields
        )