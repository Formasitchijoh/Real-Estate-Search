
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView
from .models import BookMark
from .serializers import BookMarkSerializer,BookMarkDetailSerializer,CreateBookmarkSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BookMark
from users.models import User
from listings.models import Listing
from listings.serializers import ListingSerializer, ListingDetailSerializer
# Create your views here.


class BookMarksListView(ListAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    lookup_field = 'id'

class BookMarkView(RetrieveAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkDetailSerializer
    lookup_field ='id'


class CreateBookmarkView(APIView):
    print('helloworld to me')
    def post(self, request, *args, **kwargs):
        print( request.data.get('listing_id'))
        user = User.objects.get(id=request.data.get('user_id'))
        listing = Listing.objects.get(id=request.data.get('listing_id'))
        print(listing)
        data = {
            'listing': [request.data.get('listing_id')],
            'user': request.data.get('user_id')
        }
        serializer = CreateBookmarkSerializer(data=data)
        print(serializer)
        #serializer = self.get_serializer(data={
        #    'user': user_id,
         #   'listing': listing.id
        #})
        
        serializer.is_valid(raise_exception=True)
        bookmark = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(bookmark.data, status=status.HTTP_201_CREATED, headers=headers)

