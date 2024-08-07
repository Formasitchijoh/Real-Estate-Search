from django.http import JsonResponse
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
from recommendations.models import Recommendation
from rest_framework.decorators import api_view

from .views import Images
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from rest_framework import status
# Create your views here.


class ListingPagination(PageNumberPagination):
    page_size = 12
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

from django.db.models import Q

class FullSearchListingView(viewsets.ViewSet):
    serializer_class = ListingSerializer
    def list(self,request):
        query = self.request.query_params.get('query', '')
        print(query)
        listings = Listing.objects.filter(
            Q(price__icontains=query) |
            Q(bathrooms__icontains=query) |
            Q(bedroom__icontains=query) |
            Q(listing_type__icontains=query) |
            Q(town__icontains=query) |
            Q(location__icontains=query) |
            Q(title__icontains=query)
        )
        print('\n\n', listings)
        serializer = ListingSerializer(listings, many=True)
        if serializer:
            search_results = {
            "Listings":listings,
            } 
            return Response(serializer.data, status=status.HTTP_200_OK)  


class ImageView(viewsets.ViewSet):
    def list(self, request):
        listing_id = int(self.request.query_params.get('id', ''))
        if listing_id:
            print('I am inohhh good for you', int(listing_id))
            listing_images= Images(listing_id)      
            print('I am inohhh good for you', listing_images)
            return Response(listing_images)
        return Response([])


from .documents import ListingDocument
from .serializers import ListingSerializer

from .documents import ListingDocument
from .serializers import ListingSerializer
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django_elasticsearch_dsl.search import Search
from elasticsearch_dsl import Search, Q

class ListingsSearch(APIView):
    serializer_class = ListingWithImagesSerializer
    document_class = ListingDocument

    def get(self, request):
        # Get the search parameters from the request
        query = request.query_params.get('query', None)
        bedroom = request.query_params.get('bedroom', None)
        bathrooms = request.query_params.get('bathrooms', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        listing_type = request.query_params.get('listing_type', None)

        # Create a Search object
        s = Search(index=ListingDocument._index._name)

        # Add the match query for the title
        s = s.query("match", title={"query": query, "fuzziness": "auto"})

        # Add the filter clauses
        if bedroom:
            s = s.filter("term", bedroom=bedroom)
        if bathrooms:
            s = s.filter("term", bathrooms=bathrooms)
        if min_price and max_price:
            s = s.filter("range", price={"gte": min_price, "lte": max_price})
        if listing_type:
            s = s.filter("term", listing_type=listing_type)

        # Execute the search and get the results
        response = s.execute()

        # Serialize the results
        serializer = self.serializer_class(response.hits, many=True)
        for listing in serializer.data:
            listing_images = Images(listing['id'])
            listing['listing_image'] = listing_images
            print(listing)

        return Response(serializer.data)


from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SuggesterFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet


from .documents import ListingDocument
from .serializers import ListingSerializer

class ListingDocumentViewSet(DocumentViewSet):
    document =ListingDocument
    serializer_class = ListingSerializer

    filter_backends = (
        FilteringFilterBackend,
        SuggesterFilterBackend,
        CompoundSearchFilterBackend
    )

    search_fields = ("listing_type","title","town","location")

    filter_fields = {
        "id": {"field": "id", "lookups": [LOOKUP_QUERY_IN]},
        "price": {"field": "price", "lookups": [LOOKUP_QUERY_GTE, LOOKUP_FILTER_RANGE]},
    }


    suggester_fields = {
        "listing_type_suggest": {"field": "listing_type.suggest", "suggesters": [SUGGESTER_COMPLETION]},
        "title_suggest": {"field": "title.suggest", "suggesters": [SUGGESTER_COMPLETION]},
        "town_suggest": {"field": "town.suggest", "suggesters": [SUGGESTER_COMPLETION]},
        "location_suggest": {"field": "location.suggest", "suggesters": [SUGGESTER_COMPLETION]},
    }

@api_view(['GET'])
def get_suggestions(request):
    query = request.GET.get('q', '')
    if not query:
        return Response([])

    search = ListingDocument.search()

    search = search.suggest(
        'title_suggestions',
        query,
        completion={
            "field": "title.suggest",
            "fuzzy": {
                "fuzziness": 2
            },
            "size": 5
        }
    ).suggest(
        'listing_type_suggestions',
        query,
        completion={
            "field": "listing_type.suggest",
            "fuzzy": {
                "fuzziness": 2
            },
            "size": 5
        }
    ).suggest(
        'town_suggestions',
        query,
        completion={
            "field": "town.suggest",
            "fuzzy": {
                "fuzziness": 2
            },
            "size": 5
        }
    ).suggest(
        'location_suggestions',
        query,
        completion={
            "field": "location.suggest",
            "fuzzy": {
                "fuzziness": 2
            },
            "size": 5
        }
    )

    response = search.execute()

    suggestions = set()
    for suggest in ['title_suggestions', 'listing_type_suggestions', 'town_suggestions', 'location_suggestions']:
        for option in response.suggest[suggest][0].options:
            suggestions.add(option.text)

    return Response(list(suggestions))
#########################'class ListingsListView(ViewSet):
class ListViews(viewsets.ViewSet):
    def list(self, request):
        s = Search(index='listings')
        response = s.execute()

        listing_ids = [hit.id for hit in response.hits]
        image_qs = Image.objects.filter(listing_id__in=listing_ids)
        image_dict = {}
        for image in image_qs:
            if image.listing_id in image_dict:
                image_dict[image.listing_id].append(image)
            else:
                image_dict[image.listing_id] = [image]

        serializer_data = []
        for hit in response.hits:
            listing_data = hit.to_dict()
            listing_data['listing_image'] = image_dict.get(hit.id, [])
            serializer_data.append(listing_data)

        serializer = ListingWithImagesSerializer(serializer_data, many=True)
        return Response(serializer.data)

class ContentBasedRecommendationListView(APIView):
    def get(self, request):
        # Get the search parameters from the request
        user_id = self.request.query_params.get('user_id', '')
        if user_id:
            users_recommendation = Recommendation.objects.filter(user=user_id).order_by("-created_at").first()
            #print('\n\n users interest', users_recommendation)

            if users_recommendation:
                listing_id = users_recommendation.interest_id
                #print('\n\n users interest', listing_id)
                listing = Listing.objects.get(id=listing_id)
                #print('\n\n users interest', listing.bathrooms)
                query = users_recommendation.last_search
                bedroom = listing.bedroom
                bathrooms = listing.bathrooms
                min_price = 0.0
                max_price = listing.price
                listing_type = listing.listing_type
                location = users_recommendation.location
                print('\n\n users interest', query,'\n',bedroom, '\n',bathrooms,'\n',min_price, '\n', max_price, '\n', listing_type,location)


                # Create a Search object
                s = Search(index=ListingDocument._index._name)

                # Add the match query for the title
                s = s.query("match", town={"query": users_recommendation.location, "fuzziness": "auto"})
                print('s\n\n',s.execute())

                # Add the filter clauses
                if bedroom:
                   s = s.filter("term", bedroom=bedroom)
                if bathrooms:
                   s = s.filter("term", bathrooms=bathrooms)
                if min_price and max_price:
                  s = s.filter("range", price={"gte": min_price, "lte": max_price})

                # Execute the search and get the results
                response = s.execute()

                listing_ids = [hit.id for hit in response.hits]
                image_qs = Image.objects.filter(listing_id__in=listing_ids)
                image_dict = {}
                for image in image_qs:
                    if image.listing_id in image_dict:
                        image_dict[image.listing_id].append(image)
                    else:
                        image_dict[image.listing_id] = [image]

                serializer_data = []
                for hit in response.hits:
                    listing_data = hit.to_dict()
                    listing_data['listing_image'] = image_dict.get(hit.id, [])
                    serializer_data.append(listing_data)

                serializer = ListingWithImagesSerializer(serializer_data, many=True)
                return Response(serializer.data)

def get_distinct_values(request):
    distinct_values = {
        'listing_types': list(Listing.objects.values_list('listing_type', flat=True).distinct()),
        'bedrooms': list(Listing.objects.values_list('bedroom', flat=True).distinct()),
        'bathrooms': list(Listing.objects.values_list('bathrooms', flat=True).distinct()),
        'locations': list(Listing.objects.values_list('location', flat=True).distinct()),
        'towns': list(Listing.objects.values_list('town', flat=True).distinct()),
        'prices': list(Listing.objects.values_list('price', flat=True).distinct()),
        'pricepermonth': list(Listing.objects.values_list('pricepermonth', flat=True).distinct()),
        'views': list(Listing.objects.values_list('views', flat=True).distinct()),
        'reactions': list(Listing.objects.values_list('reactions', flat=True).distinct()),
    }
    return JsonResponse(distinct_values)

def get_locations_by_town(request):
    town = request.GET.get('town')
    if town:
        town = town.strip()  # Normalize the input by stripping spaces
        print(f"Normalized town: '{town}'")  # Debugging line
        distinct_locations = Listing.objects.filter(town__iexact=town).values_list('location', flat=True).distinct()
        print(f"Distinct locations: {list(distinct_locations)}")  # Debugging line
        return JsonResponse({'locations': list(distinct_locations)})
    else:
        print("No town parameter provided")  # Debugging line
        return JsonResponse({'error': 'Town parameter is required'}, status=400)