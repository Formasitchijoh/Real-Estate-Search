
from rest_framework import viewsets
from accounts.permissions import IsClient, IsAgent
from .models import Recommendation
from rest_framework.response import Response
from .serializers import RecommendationSerializer
from listings.utils import similarity_check,Images
from rest_framework import status
from rest_framework.response import Response
from .utils import calculate_user_similarity, generate_recommendations
# Create your views here.
from rest_framework.pagination import PageNumberPagination
from listings.serializers import ListingWithImagesSerializer
from rest_framework.views import APIView

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
            print('the recommendation object:', users_recommendation.last_search)
            if users_recommendation:
                print('the recommendation string:', str(users_recommendation).replace(',', ''))
                top_listings, top_scores = similarity_check(str(users_recommendation).replace(',', ''))
                search_results = {
                    "Listings": top_listings,
                    "Scores": top_scores
                }
                return Response(search_results, status=status.HTTP_200_OK)
        return Response([])


# views.py



class UserRecommendationViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            similar_users = calculate_user_similarity(user_id)
            
            # Aggregate recommendations from similar users
            recommendations = []
            for similar_user, similarity_score in similar_users:
                user_recommendations = Recommendation.objects.filter(user=similar_user)[:5]  # Limit to top 5 recommendations per user
                for rec in user_recommendations:
                    recommendations.append({
                        'user': similar_user.user.username,
                        'recommendation_text': rec.recommendation_text,
                        'similarity_score': similarity_score
                    })
            
            # Sort recommendations by similarity score (descending)
            recommendations = sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)
            
            return Response(recommendations)
        else:
            return Response([])



class UserRecommendationsView(viewsets.ViewSet):
    def list(self, request):
        try:
            user_id = request.query_params.get('user_id')
            print('\n\nvalue of the user\n', user_id)
            recommendations = generate_recommendations(user_id)
            serializer = ListingWithImagesSerializer(recommendations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)