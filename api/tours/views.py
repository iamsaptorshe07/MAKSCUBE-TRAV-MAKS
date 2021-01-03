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
    print("\nApi Entered\n")
    tour1 = request.GET.get('tour1')
    tour2 = request.GET.get('tour2')
    tourList=-1
    try:
        tour3 = request.GET.get('tour3')
        tourList=tourList+1
    except:
        print("Tour3 is not here... :|")
    try:
        tour4 = request.GET.get('tour4')
        tourList=tourList+1
    except:
        print("Tour4 is not here... :|")
    if tourList==-1 :
        tour_data = Tour.objects.filter(Q(tourId=tour1) | Q(tourId=tour2))
    elif tourList==0:
        tour_data = Tour.objects.filter(Q(tourId=tour1) | Q(tourId=tour2) | Q(tourId=tour3))
    elif tourList==1:
        tour_data = Tour.objects.filter(Q(tourId=tour1) | Q(tourId=tour2) | Q(tourId=tour3) | Q(tourId=tour4))

    print(tour_data)
    data = TourSerializer(tour_data, many=True)
    print("\n\n",data.data,"\n\n")
    return Response(
        {
            'status':200,
            'tour_data':data.data
        }
    )

class SearchTour(APIView):
    def get(self,request):
        try:
            sLocation = request.GET.get('sLocation')
            eLocation = request.GET.get('eLocation')
        except Exception as problem:
            return Response(
                {
                    'status':406,
                    'message':problem
                },
                status = status.HTTP_406_NOT_ACCEPTABLE
            )
        if sLocation != None and eLocation != None:
            tour1 = Tour.objects.filter(startingLocation__icontains=sLocation,endLocation__icontains=eLocation,publish_mode = True,
            last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1)
            tour2 = Tour.objects.filter(Q(tourHeading__icontains = sLocation) | Q(tourHeading__icontains = eLocation),publish_mode = True,
                last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1)
            tours = tour1.union(tour2)
            tour_data = TourSerializer(tours,many=True)
            return Response(
                {
                    'status':200,
                    'tours':tour_data.data
                },
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'status':406,
                    'message':"sLocation and eLocation can not be NULL"
                },
                status = status.HTTP_406_NOT_ACCEPTABLE
            )

class AdvancedSearch(APIView):
     def get(self,request):
        try:
            startLocSearch = request.GET.get('startLocSearch')
            endLocSearch = request.GET.get('endLocSearch')
            startDateSearch = request.GET.get('startDateSearch')
            endDateSearch = request.GET.get('endDateSearch')
            startPrice= request.GET.get('startPrice')
            endPrice = request.GET.get('endPrice')
            minDuration=request.GET.get('minDuration')
            maxDuration = request.GET.get('maxDuration')
        except Exception as problem:
            return Response(
                {
                    'status':406,
                    'message':problem
                },
                status = status.HTTP_406_NOT_ACCEPTABLE
            )
        tour1 = Tour.objects.filter(startingLocation__icontains=startLocSearch,endLocation__icontains=endLocSearch,
        publish_mode = True,startDate__gte=startDateSearch,endDate__lte=endDateSearch,price__gte=startPrice,price__lte=endPrice,
        last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1)
        tours = []
        for i in tour1:
            day = i.startDate - i.endDate
            if day>=minDuration and day<=maxDuration:
                tours.append(i)
        tour_data = TourSerializer(tours,many=True)
        return Response(
            {
                'status':200,
                'tours':tour_data.data
            },
            status = status.HTTP_200_OK
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
    
    


