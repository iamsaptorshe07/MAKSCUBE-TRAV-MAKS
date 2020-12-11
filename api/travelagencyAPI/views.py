from django.shortcuts import render

from travelagency.models import Tour

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


        
