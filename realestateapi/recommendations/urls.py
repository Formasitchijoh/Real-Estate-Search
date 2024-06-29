from django.urls import path, include
from .views import RecommendationListView,UserRecommendationListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'list', RecommendationListView)
router.register(r'user', UserRecommendationListView, basename='user')


urlpatterns =[
    path('', include(router.urls)),
]

