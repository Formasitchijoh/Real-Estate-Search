from django.urls import path, include
from .views import ListingsListView,ProcessedListingView,SearchView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'processed',  ProcessedListingView)
router.register(r'list', ListingsListView)
router.register(r'search', SearchView, basename='search')


urlpatterns =[
    path('', include(router.urls)),
]

