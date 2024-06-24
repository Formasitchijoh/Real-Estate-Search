from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
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

    def __str__(self):
        return self.title

class ProcessedListings(models.Model):
    query = models.CharField(max_length=255, default="")
    Unnamed = models.IntegerField()
    title = models.CharField(max_length=255)
    image = models.URLField()
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

    def __str__(self):
        return f"{self.title} - {self.location}"
    

class Query(models.Model):
    query = models.CharField(max_length=50, default='')
    listing = models.ManyToManyField(Listing)

    class Meta:
        db_table = 'querys'

    def __str__(self):
        return self.query