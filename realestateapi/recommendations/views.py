
from rest_framework import viewsets
from accounts.permissions import IsClient, IsAgent
from .models import Recommendation
from rest_framework.response import Response
from .serializers import RecommendationSerializer
from listings.utils import similarity_check,Images
from rest_framework import status
# Create your views here.
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class RecommendationPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class RecommendationListView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    #permission_classes = [IsClient]
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    pagination_class = RecommendationPagination
    http_method_names=['get','post','option','put']

class UserRecommendationListView(viewsets.ViewSet):
    def list(self, request):
        user_id = self.request.query_params.get('user_id', '')
        print('user id for recommendation', user_id)
        if user_id:
            users_recommendation = Recommendation.objects.filter(user=user_id).order_by("-created_at").first()
            print( 'the recommedation string',str(users_recommendation).replace(',', ''))
            top_listings, top_scores = similarity_check(str(users_recommendation).replace(',', ''))  
            search_results = {
            "Listings":top_listings,
            "Scores":top_scores
            }        
            return Response(search_results, status=status.HTTP_200_OK)
        return Response([])
    