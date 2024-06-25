from django.db import models
from accounts.models import User
# Create your models here.


class Recommendations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    last_search = models.CharField(max_length=50)

    class Meta:
        db_table = 'recommendations'
    
    def __str__(self):
        return self.user