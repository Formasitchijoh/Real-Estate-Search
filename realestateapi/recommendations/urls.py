from django.urls import path, include
from .views import RecommendationListView,UserRecommendationListView
from rest_framework import routers
from .views import UserRecommendationViewSet, UserRecommendationsView

router = routers.DefaultRouter()
router.register(r'list', RecommendationListView)
router.register(r'user', UserRecommendationListView, basename='user')
router.register(r'user-recommendations', UserRecommendationViewSet, basename='user-recommendations')
router.register(r'rec', UserRecommendationsView, basename='rec')


urlpatterns =[
    path('', include(router.urls)),
]

