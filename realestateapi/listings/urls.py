from django.urls import path
from .views import ListingsListView, ListingView
from django.urls import path

urlpatterns =[
    path('', ListingsListView.as_view()),
    path('<int:id>', ListingView.as_view())
]

