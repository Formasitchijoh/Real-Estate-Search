from rest_framework import serializers
from .models import Recommendation

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ('user','location','interest')
