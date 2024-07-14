from django.urls import path, include
from .views import ListingsListView,ProcessedListingView,SearchView, ImageView, FullSearchListingView, ListingsSearch, ListingDocumentViewSet,ContentBasedRecommendationListView, get_distinct_values, get_locations_by_town
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'processed',  ProcessedListingView)
router.register(r'list', ListingsListView)
router.register(r'search', SearchView, basename='search')
router.register(r'images', ImageView, basename='image')
router.register(r'fullsearch', FullSearchListingView, basename='fullsearch')
router.register(r'listing_document', ListingDocumentViewSet, basename="listing_document")


urlpatterns =[
    path('', include(router.urls)),
    path("listing_search/", ListingsSearch.as_view()),
    path("content/", ContentBasedRecommendationListView.as_view()),
    path('distinct-values/', get_distinct_values, name='distinct-values'),
    path('locations/', get_locations_by_town, name='locations-by-town'),

]

