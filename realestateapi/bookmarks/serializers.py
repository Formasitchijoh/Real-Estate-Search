from rest_framework import serializers
from .models import BookMark
from listings.models import Listing
from users.models import User
class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = ('id','listing','user')

class BookMarkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = ('id','listing','user')
        lookup_field = 'id'


class CreateBookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookMark
        fields = ['listing', 'user']

    def create(self, validated_data):
        listing = validated_data.pop('listing')
        user = validated_data.pop('user')
        print(listing, user)
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
