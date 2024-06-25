
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView
from .models import BookMark
from .serializers import BookMarkSerializer,BookMarkDetailSerializer
from .models import BookMark
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework import viewsets

# Create your views here.


class BookMarksListView(viewsets.ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    http_method_names=['get','post','option','put']
    lookup_field = 'id'

class BookMarkView(viewsets.ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkDetailSerializer
    http_method_names=['get','post','option','put']
    lookup_field ='id'


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

