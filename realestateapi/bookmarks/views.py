
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView
from .models import BookMark
from .serializers import BookMarkSerializer,BookMarkDetailSerializer,CreateBookmarkSerializer
from .models import BookMark
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here

# Create your views here.


class BookMarksListView(CreateAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    lookup_field = 'id'

class BookMarkView(RetrieveAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkDetailSerializer
    lookup_field ='id'


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

