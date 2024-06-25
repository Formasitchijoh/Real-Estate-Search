from django.urls import path, include
from .views import RecommendationListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'',RecommendationListView)


urlpatterns =[
    path('', include(router.urls)),
]

