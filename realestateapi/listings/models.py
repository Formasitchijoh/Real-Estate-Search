from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=1000, name='title')
    image = models.CharField(max_length=500)
    link = models.CharField(max_length=200)
    listing_type = models.CharField(max_length=50)
    bedroom = models.CharField(max_length=200)
    bathrooms = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    price = models.CharField(max_length=200)
    pricepermonth = models.CharField(max_length=50)
    views = models.CharField(max_length=200)
    reactions = models.IntegerField()

    def __str__(self):
        return self.title