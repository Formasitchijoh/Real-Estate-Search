from rest_framework import serializers
from . import models


#creating an serializer for my model

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Listing
        fields = '__all__'

class BookMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookMark
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inquiry
        fields = '__all__'

class InquiryMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InquiryMessage
        fields = '__all__'

class RealEstateAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.RealEstateAgent
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = '__all__'

