from django.db import models
from accounts.models import User
from listings.models import Listing
# Create your models here.


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    interest = models.ForeignKey(Listing, on_delete=models.CASCADE)
    last_search = models.CharField(max_length=50, default='nothing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recommendations'
    
    def __str__(self):
        return f"{self.last_search, self.location, self.interest}"