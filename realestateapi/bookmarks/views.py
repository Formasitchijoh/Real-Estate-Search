
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView
from .models import BookMark
from .serializers import BookMarkSerializer,BookMarkDetailSerializer
from .models import BookMark
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework import viewsets
from accounts.models import User
from rest_framework import status
from listings.serializers import ProcessedListingSerializer
from listings.models import Image

# Create your views here.

class BookMarksListView(viewsets.ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    http_method_names = ['get', 'post', 'option', 'put']
    lookup_field = 'id'
    from django.db.models import Prefetch
    def list(self, request, *args, **kwargs):
        user = self.request.query_params.get('user_id', '')
        bookmarks = BookMark.objects.filter(user=user).prefetch_related('listing')
        listings = []
        for bookmark in bookmarks:
            listings.extend(bookmark.listing.all())
            #print('\nin\n',bookmark.listing.all())
        serializer = ProcessedListingSerializer(listings, many=True)
        bookMarkedListing = []
        for listing in serializer.data:
            print(listing['listing'])
            listing_id = listing['listing']
            images = Image.objects.filter(listing_id=listing_id)
            listing_with_images = listing.copy()
            listing_with_images['images'] = [image.image for image in images]
            bookMarkedListing.append(listing_with_images)
        print(bookMarkedListing)
        return Response(bookMarkedListing, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        listing_ids = request.data.get('listing', [])

        try:
            bookmark = BookMark.objects.filter(user=user).order_by('-id').first()
            if bookmark:
                for listing_id in listing_ids:
                    bookmark.listing.add(listing_id)
                bookmark.save()
                serializer = self.get_serializer(bookmark)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                request.data['user'] = user
                request.data['listing'] = listing_ids
                return super().create(request, *args, **kwargs)
        except (BookMark.DoesNotExist, IndexError):
            request.data['user'] = user
            request.data['listing'] = listing_ids
            return super().create(request, *args, **kwargs)
        
class UserBookMarkListView(viewsets.ModelViewSet):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkDetailSerializer
    http_method_names=['get','post','option','put']
    lookup_field = 'id'

    from django.db.models import Prefetch

    def list(self, request, *args, **kwargs):
        user = self.request.query_params.get('user_id', '')
        bookmarks = BookMark.objects.filter(user=user).prefetch_related('listing')
        print(bookmarks)
        listings = []
        for bookmark in bookmarks:
            listings.extend(bookmark.listing.all())
        serializer = ProcessedListingSerializer(listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

