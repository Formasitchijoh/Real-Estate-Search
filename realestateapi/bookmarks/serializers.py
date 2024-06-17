from rest_framework import serializers
from .models import BookMark
class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = ('id','listing','user')

class BookMarkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = ('id','listing','user')
        lookup_field = 'id'