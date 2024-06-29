from rest_framework.response import Response
from .models import Listing, ProcessedListings, Image
from .serializers import ListingSerializer, ProcessedListingSerializer, ListingImageSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework import viewsets
from .utils import similarity_check,Images
from accounts.permissions import IsClient, IsAgent
from rest_framework.views import APIView

# Create your views here.
        
class ListingsListView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    #permission_classes = [IsClient]
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

class ImageViews(viewsets.ViewSet):
    def list(self, request):
        print('I am inohhh')
        listing_images = []
        listing_id = int(self.request.query_params.get('id', ''))
        print('I am inohhh',listing_id)
        try:
            images = Image.objects.filter(listing_id=listing_id)
            print(images)
            for image in images:
                serializer = ListingSerializer(image)
                if serializer.is_valid():
                   listing_images.append(image)
                   print('\nlisting image\n', listing_images)
            return listing_images
        except:
            print('')

        return Response(listing_images)


class ImageView(viewsets.ViewSet):
    def list(self, request):
        print('I am inohhh')
        listing_id = int(self.request.query_params.get('id', ''))
        if listing_id:
            print('I am inohhh good for you', int(listing_id))
            listing_images= Images(listing_id)      
            print('I am inohhh good for you', listing_images)
            return Response(listing_images)
        return Response([])