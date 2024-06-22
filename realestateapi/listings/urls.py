from django.urls import path, include
from .views import ListingsListView,ProcessedListingView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'',  ListingsListView)
router.register(r'processed',  ProcessedListingView)

urlpatterns =[
    path('', include(router.urls)),
]

