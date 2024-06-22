from rest_framework import serializers
from .models import Listing, ProcessedListings
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('id', 'title', 'image', 'link', 'listing_type', 'bedroom', 'bathrooms', 'location', 'town', 'price', 'pricepermonth', 'views', 'reactions')
        lookup_field = 'id'

        
class ProcessedListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedListings
        fields = '__All__'