from django.urls import path,include
from .views import BookMarksListView
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', BookMarksListView)
urlpatterns =[
    path('', include(router.urls)),


]

