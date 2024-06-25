from django.db import models
from listings.models import ProcessedListings
from accounts.models import User
# Create your models here.


class BookMark(models.Model):
    listing = models.ManyToManyField(ProcessedListings, related_name='bookmarkedListing')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'bookmarks'
    
    def __str__(self):
        return self.listing