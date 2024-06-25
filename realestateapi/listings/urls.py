from django.urls import path, include
from .views import ListingsListView,ProcessedListingView,SearchView, ImageView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'processed',  ProcessedListingView)
router.register(r'list', ListingsListView)
router.register(r'search', SearchView, basename='search')
router.register(r'images', ImageView, basename='image')


urlpatterns =[
    path('', include(router.urls)),
]

