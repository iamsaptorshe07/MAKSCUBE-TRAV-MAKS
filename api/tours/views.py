from django.shortcuts import render
from rest_framework.response import Response
from .serializers import TourSerializer,TourImageSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from travelagency.models import Tour, TourImage
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
import datetime
from django.db.models import Q
# Create your views here.

class TourAPIView(ListAPIView):
    queryset = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1)
    serializer_class = TourSerializer
    pagination_class = PageNumberPagination


@api_view(['GET'])
def TourDetailsAPIView(request,slug):
    try:
        tour = Tour.objects.get(tourSlug=slug)
        tourimages =TourImage.objects.get(tour=tour)
    except Exception as e:
        print(e)
        exception = {
            'status':404,
            'message':'Does Not Exist'
        }
        return Response(request,exception)
    data1 = TourSerializer(tour)
    data2 = TourImageSerializer(tourimages)
    main_data = {
        'tourdata':data1.data,
        'tourimages':data2.data,
    }
    return Response(main_data)
    
    
    

