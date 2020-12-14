from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from travelagency.models import Tour, TourImage
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from api.travelagencyAPI.serializers import TourSerializer, TourImageSerializer
import datetime
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

class TourAPIView(ListAPIView):
    queryset = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1)
    serializer_class = TourSerializer
    pagination_class = PageNumberPagination


@api_view(['GET'])
def compareTourView(request):
    print("\nEntered\n")
    tour1 = int(request.GET.get('tour1'))
    tour2 = int(request.GET.get('tour2'))
    tour3 = int(request.GET.get('tour3'))
    tour4 = int(request.GET.get('tour4'))
    tour_data = Tour.objects.filter(Q(id=tour1) | Q(id=tour2) | Q(id=tour3) | Q(id=tour4)) 
    print(tour_data)
    data = TourSerializer(tour_data, many=True)
    print("\n\n",data.data,"\n\n")
    return Response(
        {
            'status':200,
            'tour_data':data.data
        }
    )



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
        return Response(data=exception,status = status.HTTP_404_NOT_FOUND)
    data1 = TourSerializer(tour)
    data2 = TourImageSerializer(tourimages)
    description_data = data1.data['description'].split('@@@@')
    description = []
    for i in description_data:
        lst = i.split('$$$$')
        description.append(lst)
    day_title = []
    day_description = []
    for i in description:
        day_title.append(i[0])
        day_description.append(i[1])
    data1 = dict(data1.data)
    data1['description']={
        'day_title':day_title,
        'day_description':day_description
    }
    link = 'http://'+ str(get_current_site(request).domain)
    images = list(dict(data2.data.items()).values())
    mimg = []
    for i in range(1,len(images)-1):
        if(images[i]!=None):
            images[i]=link+str(images[i])
            mimg.append(images[i])
    main_data = {
        'tourdata':data1,
        'tourimages':mimg,
        'weblink':link
    }
    return Response(data = main_data, status = status.HTTP_200_OK)
    
    


