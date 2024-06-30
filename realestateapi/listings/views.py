from rest_framework.response import Response
from .models import Listing, ProcessedListings, Image
from .serializers import ListingSerializer, ProcessedListingSerializer,ListingWithImagesSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework import viewsets
from .utils import similarity_check,Images
from accounts.permissions import IsClient, IsAgent
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ListingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ListingsListView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    #permission_classes = [IsClient]
    queryset = Listing.objects.all().prefetch_related('listing_image')
    serializer_class = ListingWithImagesSerializer
    pagination_class = ListingPagination
    http_method_names = ['get', 'post', 'option', 'put']

    def get_queryset(self):
        # Optionally, you can add filters or annotations here
        return super().get_queryset()


class ProcessedListingView(viewsets.ModelViewSet):
    queryset = ProcessedListings.objects.all()
    serializer_class = ProcessedListingSerializer
    http_method_names = ['get', 'post','option','put']

class SearchView(viewsets.ViewSet):
    #pagination_class = ListingPagination
    def list(self, request):
        print('I am inohhh')
        search_query = self.request.query_params.get('query', '')
        if search_query:
            print('I am inohhh good for you',search_query)
            top_listings, top_scores = similarity_check(search_query) 
            search_results = {
            "Listings":top_listings,
            "Scores":top_scores
            }        
            print('I am inohhh good for you')

            return Response(search_results)
        return Response([])
        
class SearchViews(viewsets.ViewSet):
    pagination_class = ListingPagination

    def list(self, request):
        print('\n\npage\n\n')
        search_query = self.request.query_params.get('query', '')
        print('\n\npage\n\n',search_query)

        if search_query:
            top_listings, top_scores = similarity_check(search_query)
            search_results = {
                "Listings": top_listings,
                "Scores": top_scores
            }
            #page = self.pagination_class.paginate_queryset(search_results["Listings"], request)
           # if page is not None:
               # return self.pagination_class.get_paginated_response(page)
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
        listing_id = int(self.request.query_params.get('id', ''))
        if listing_id:
            print('I am inohhh good for you', int(listing_id))
            listing_images= Images(listing_id)      
            print('I am inohhh good for you', listing_images)
            return Response(listing_images)
        return Response([])