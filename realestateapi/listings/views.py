from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework import permissions
from .models import Listing, ProcessedListings
from .serializers import ListingSerializer, ProcessedListingSerializer
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated  # <-- Here

from rest_framework import viewsets

# Create your views here.
        
class ListingsListView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)             # <-- And here
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    http_method_names=['get','post','option','put']

class ProcessedListingView(viewsets.ModelViewSet):
    queryset = ProcessedListings.objects.all()
    serializer_class = ProcessedListingSerializer
    http_method_names = ['get', 'post','option','put']