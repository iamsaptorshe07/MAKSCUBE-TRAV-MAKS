from django.shortcuts import render

from travelagency.models import Tour, TourImage

from .serializers import TourSerializer, TourImageSerializer

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication

from django.contrib.sites.shortcuts import get_current_site

class MyAgencyTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        print("\nentered\n")
        if request.session.session_key:
            if request.session['access_type']=='seller':
                tour = Tour.objects.filter(seller=request.user)
                print("\n\n",tour,"\n\n")
                tourSerializer = TourSerializer(tour,many=True)
                for i in tourSerializer.data:
                    i['thumbnail']=str('http://')+str(get_current_site(request).domain)+str(i['thumbnail'])
                return Response(
                    {
                        'status':200,
                        'tours':tourSerializer.data,
                        'weblink':get_current_site(request).domain
                    }
                )
            else:
                return Response(
                    {
                        'status':404,
                        'message':'Not Authorized'
                    }
                )
        else:
            return Response(
                {
                    'status':404,
                    'message':'Not Authenticated'
                }
            )


        
class TourDetail(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request,tourId):
        try:
            tour = Tour.objects.get(tourId=tourId)
            tourimages =TourImage.objects.get(tour=tour)
        except Exception as e:
            print(e)
            exception = {
                'status':404,
                'message':'Does Not Exist'
            }
            return Response(exception,status = status.HTTP_404_NOT_FOUND)
        data1 = TourSerializer(tour)
        data2 = TourImageSerializer(tourimages)
        data2 = dict(data2.data)
        images = data2.items()
        link = get_current_site(request)
        main_data = {
            'tourdata':data1.data,
            'tourimages':images,
            'weblink':link.domain
        }
        return Response(main_data)