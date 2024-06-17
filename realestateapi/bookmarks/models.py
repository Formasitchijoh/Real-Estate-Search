from django.db import models
from backend.models import Listing
from users.models import User
# Create your models here.


class BookMark(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ManyToManyField(Listing)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.listing