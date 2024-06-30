from rest_framework import serializers
from .models import Listing, ProcessedListings, Image
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('id', 'title', 'link', 'listing_type', 'bedroom', 'bathrooms', 'location', 'town', 'price', 'pricepermonth', 'views', 'reactions')
        lookup_field = 'id'

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id','image','listing')
        
class ListingWithImagesSerializer(serializers.ModelSerializer):
    listing_image = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'link', 'listing_type', 'bedroom', 'bathrooms',
            'location', 'town', 'price', 'pricepermonth', 'views', 'reactions',
            'listing_image'
        ]

class ProcessedListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedListings
        fields = ('id', 'title','listing','link', 'listing_type', 'bedroom', 'bathrooms', 'location', 'town', 'price', 'pricepermonth', 'views', 'reactions')

