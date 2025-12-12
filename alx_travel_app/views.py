from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

# Create your views here.
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
    
    def get_queryset(self):
        queryset = Listing.objects.all()
        
        # Filter by availability
        available_only = self.request.query_params.get('available', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(is_available=True)
        
        # Filter by property type
        property_type = self.request.query_params.get('property_type', None)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        # Filter by max price
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        
        # Filter by minimum bedrooms
        min_bedrooms = self.request.query_params.get('min_bedrooms', None)
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        listing = self.get_object()
        bookings = listing.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

