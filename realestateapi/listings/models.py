from django.db import models
# Create your models here.
from django.contrib.auth.hashers import make_password

# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    listing_type = models.CharField(max_length=100)
    bedroom = models.FloatField()
    bathrooms = models.FloatField()
    location = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    price = models.FloatField()
    pricepermonth = models.CharField(max_length=500)
    views = models.IntegerField()
    reactions = models.IntegerField()

    class Meta:
        db_table = 'listings'
    def __str__(self):
        return self.title
    


# a table formed from the relationship of listings and query but it is handled and processed differently
class ProcessedListings(models.Model):
    query = models.CharField(max_length=255, default="")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField()
    listing_type = models.CharField(max_length=100)
    bedroom = models.FloatField()
    bathrooms = models.FloatField()
    location = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    price = models.FloatField()
    pricepermonth = models.CharField(max_length=500)
    views = models.IntegerField()
    reactions = models.IntegerField()

    class Meta:
        db_table = 'processed_listing'

    def __str__(self):
        return self.title

class Image(models.Model):
    image=models.URLField() 
    listing = models.ForeignKey(Listing, related_name='listing_image',on_delete=models.CASCADE)

    class Meta:
        db_table = 'listing_images'

class Query(models.Model):
    query = models.CharField(max_length=1000, default='')

    class Meta:
        db_table = 'querys'

    def __str__(self):
        return self.query