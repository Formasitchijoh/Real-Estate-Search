from django.db import models
from users.models import User
class Listing(models.Model):
    title = models.CharField(max_length=150)
    name = models.CharField(max_length=30, default="something")
    description = models.CharField(max_length=500, default="something")

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    title = models.CharField(max_length=1000, name='title')
    image = models.CharField(max_length=500, name="image")
    link = models.CharField(max_length=200)
    listing_type = models.CharField(max_length=50)
    bedroom = models.CharField(max_length=200)
    bathrooms = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    price = models.CharField(max_length=200)
    pricepermonth = models.CharField(max_length=50)
    views = models.CharField(max_length=200)
    reactions = models.IntegerField(default=0)

    def __str__(self):
       return {
        "title": self.title,
        "image": self.image,
        "link": self.link,
        "listing_type": self.listing_type,
        "bedroom": self.bedroom,
        "bathrooms": self.bathrooms,
        "location": self.location,
        "town": self.town,
        "price": self.price,
        "pricepermonth": self.pricepermonth,
        "views": self.views,
        "reactions": self.reactions
    }


class Posts(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.CharField(max_length=150)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.tags