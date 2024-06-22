from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework import permissions
from . import models
from .serializers import ListingSerializer, BookMarksSerializer,UserSerializer,InquirySerializer,InquiryMessageSerializer,RealEstateAgentSerializer,ReportSerializer
from rest_framework import viewsets

class ListingsView(viewsets.ModelViewSet):
    queryset = models.Listing.objects.all()
    serializer_class = ListingSerializer

class BookMarksView(viewsets.ModelViewSet):
    queryset = models.BookMark.objects.all()
    serializer_class = BookMarksSerializer

class InquiryView(viewsets.ModelViewSet):
    queryset = models.Inquiry.objects.all()
    serializer_class = InquirySerializer

class InquiryMessageView(viewsets.ModelViewSet):
    queryset = models.InquiryMessage.objects.all()
    serializer_class = InquiryMessageSerializer

class ReportsView(viewsets.ModelViewSet):
    queryset = models.Report.objects.all()
    serializer_class = ReportSerializer

class RealEstateAgentView(viewsets.ModelViewSet):
    queryset = models.RealEstateAgent.objects.all()
    serializer_class = RealEstateAgentSerializer






