from django.urls import path,include
from .views import BookMarksListView, UserBookMarkListView
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', BookMarksListView)
router.register(r'user', UserBookMarkListView, basename="user")
urlpatterns =[
    path('', include(router.urls)),


]

