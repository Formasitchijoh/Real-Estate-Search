from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group, Permission,AbstractUser

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

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

class BookMark(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ManyToManyField(Listing)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Inquiry(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    realestateagent = models.ForeignKey('RealEstateAgent', on_delete=models.CASCADE, related_name='inquiries')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InquiryMessage(models.Model):
    id = models.AutoField(primary_key=True)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)  # Can be 'client' or 'agent'
    message = models.TextField(max_length=1000)
    sent_at = models.DateTimeField(auto_now_add=True)

class RealEstateAgent(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    inquirys = models.ManyToManyField('Inquiry', related_name='real_estate_agents')

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    report_date = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(Admin, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing)