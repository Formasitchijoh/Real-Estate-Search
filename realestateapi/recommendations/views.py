
from rest_framework import viewsets
from accounts.permissions import IsClient, IsAgent
from .models import Recommendation
from .serializers import RecommendationSerializer
# Create your views here.
        
class RecommendationListView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    permission_classes = [IsClient]
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    http_method_names=['get','post','option','put']

