from django.db import models
from listings.models import ProcessedListings, Listing
from accounts.models import User
from recommendations.models import Recommendation
# Create your models here.


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ManyToManyField(ProcessedListings)

    class Meta:
        db_table = 'bookmarks'
    
    def __str__(self):
        return self.listing