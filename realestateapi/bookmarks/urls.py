from django.urls import path
from .views import BookMarksListView,BookMarkView, HelloView
from django.urls import path

urlpatterns =[
    path('', BookMarksListView.as_view()),
    path('<int:id>', BookMarkView.as_view()),
    path('hello/', HelloView.as_view(), name='hello'),

]
