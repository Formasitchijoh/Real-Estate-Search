from rest_framework import serializers
from .models import Listing
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('id', 'title','location', 'town', 'price', 'listing_type', 'bedroom', 'bathrooms')

class ListingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ('id', 'title', 'image', 'link', 'listing_type', 'bedroom', 'bathrooms', 'location', 'town', 'price', 'pricepermonth', 'views', 'reactions')
        lookup_field = 'id'
