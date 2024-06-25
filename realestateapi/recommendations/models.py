from django.db import models
from accounts.models import User
from listings.models import ProcessedListings
# Create your models here.


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    last_search = models.CharField(max_length=50)
    interest = models.ForeignKey(ProcessedListings, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recommendation'
    
    def __str__(self):
        return self.user