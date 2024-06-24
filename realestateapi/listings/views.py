from rest_framework.response import Response
from .models import Listing, ProcessedListings
from .serializers import ListingSerializer, ProcessedListingSerializer
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework import viewsets
from .utils import similarity_check

# Create your views here.
        
class ListingsListView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    http_method_names=['get','post','option','put']

class ProcessedListingView(viewsets.ModelViewSet):
    queryset = ProcessedListings.objects.all()
    serializer_class = ProcessedListingSerializer
    http_method_names = ['get', 'post','option','put']


class SearchView(viewsets.ViewSet):
    def list(self, request):
        print('I am inohhh')
        search_query = self.request.query_params.get('query', '')
        if search_query:
            print('I am inohhh good for you',search_query)
            top_listings, top_scores = similarity_check(search_query)
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

