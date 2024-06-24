from django.db import models
from backend.models import Listing
from users.models import User
# Create your models here.


class BookMark(models.Model):
    listing = models.ManyToManyField(Listing, related_name='bookmarkedListing')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.listing