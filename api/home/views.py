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

class RecentAddedTour(APIView):
    def get(self,request):
        data = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1).order_by('-id')
        if len(data)>10:
            data = data[0:11]
        tourSerializer = TourSerializer(data,many=True)
        for i in tourSerializer.data:
                    i['thumbnail']=str('http://')+str(get_current_site(request).domain)+str(i['thumbnail'])
        return Response(
            {
                'status':200,
                'tours':tourSerializer.data,
                'weblink':get_current_site(request).domain
            }
        )

class SoloTour(APIView):
    def get(self,request):
        data = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1,tour_type='Solo-Tour').order_by('-id')
        if len(data)>10:
            data = data[0:11]
        tourSerializer = TourSerializer(data,many=True)
        for i in tourSerializer.data:
                    i['thumbnail']=str('http://')+str(get_current_site(request).domain)+str(i['thumbnail'])
        return Response(
            {
                'status':200,
                'tours':tourSerializer.data,
                'weblink':get_current_site(request).domain
            }
        )

class CoupleTour(APIView):
    def get(self,request):
        data = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1,tour_type='Couple-Friendly').order_by('-id')
        if len(data)>10:
            data = data[0:11]
        tourSerializer = TourSerializer(data,many=True)
        for i in tourSerializer.data:
                    i['thumbnail']=str('http://')+str(get_current_site(request).domain)+str(i['thumbnail'])
        return Response(
            {
                'status':200,
                'tours':tourSerializer.data,
                'weblink':get_current_site(request).domain
            }
        )

class FamilyTour(APIView):
    def get(self,request):
        data = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1,tour_type='Family-Special').order_by('-id')
        if len(data)>10:
            data = data[0:11]
        tourSerializer = TourSerializer(data,many=True)
        for i in tourSerializer.data:
                    i['thumbnail']=str('http://')+str(get_current_site(request).domain)+str(i['thumbnail'])
        return Response(
            {
                'status':200,
                'tours':tourSerializer.data,
                'weblink':get_current_site(request).domain
            }
        )

class FriendsTour(APIView):
    def get(self,request):
        data = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1,tour_type='Friends-Special').order_by('-id')
        if len(data)>10:
            data = data[0:11]
        tourSerializer = TourSerializer(data,many=True)
        for i in tourSerializer.data:
                    i['thumbnail']=str('http://')+str(get_current_site(request).domain)+str(i['thumbnail'])
        return Response(
            {
                'status':200,
                'tours':tourSerializer.data,
                'weblink':get_current_site(request).domain
            }
        )

