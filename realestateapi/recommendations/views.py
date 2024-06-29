
from rest_framework import viewsets
from accounts.permissions import IsClient, IsAgent
from .models import Recommendation
from rest_framework.response import Response
from .serializers import RecommendationSerializer
from listings.utils import similarity_check,Images
# Create your views here.
        
class RecommendationListView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    #permission_classes = [IsClient]
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    http_method_names=['get','post','option','put']

class UserRecommendationListView(viewsets.ViewSet):
    print('I am inohhh')
    def list(self, request):
        print('I am inohhh')
        user_id = self.request.query_params.get('user_id', '')
        if user_id:
            users_recommendation = Recommendation.objects.filter(user=user_id).order_by("-created_at").first()
            print('I am inohhh good for you',str(users_recommendation).replace(',', ''))
            top_listings, top_scores = similarity_check(str(users_recommendation).replace(',', ''))
            #search_results = [
              #  {'id': listing.id, 'title': listing.title, 'description': listing.description, 'score': score}
               # for listing, score in zip(top_listings, top_scores)
            #]  
            search_results = {
            "Listings":top_listings,
            "Scores":top_scores
            }        
            print('I am inohhh good for you')

            return Response(search_results)
        return Response([])