from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions
from .models import Listing
from .serializers import ListingSerializer, ListingDetailSerializer
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from django.conf import settings
# Create your views here.

class JWTAuthentication(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Authorization', '').split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['id']
            request.user_email = payload['email']
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False
        
class ListingsListView(ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'id'

class ListingView(RetrieveAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingDetailSerializer
    lookup_field ='id'