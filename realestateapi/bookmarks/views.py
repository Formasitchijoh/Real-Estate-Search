
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import BookMark
from .serializers import BookMarkSerializer,BookMarkDetailSerializer
# Create your views here.


class BookMarksListView(ListAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    lookup_field = 'id'

class BookMarkView(RetrieveAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkDetailSerializer
    lookup_field ='id'