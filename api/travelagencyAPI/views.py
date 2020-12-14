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
        if request.session.session_key:
            if request.session['access_type']=='seller':
                try:
                    tour = Tour.objects.get(tourId=tourId,seller=request.user)
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
                return Response(data = main_data,status=status.HTTP_200_OK)
            else:
                return Response(data={'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'message':'Not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,tourId):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                try:
                    tour = Tour.objects.get(tourId=tourId,seller=request.user)
                    tourimages =TourImage.objects.get(tour=tour)
                except Exception as e:
                    print(e)
                    exception = {
                        'status':404,
                        'message':'Does Not Exist'
                    }
                    return Response(exception,status = status.HTTP_404_NOT_FOUND)
                    # Start writting your editting logic
            else:
                return Response(data={'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'message':'Not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,tourId):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                try:
                    tour = Tour.objects.get(tourId=tourId,seller=request.user)
                except Exception as e:
                    print(e)
                    exception = {
                        'status':404,
                        'message':'Does Not Exist'
                    }
                    return Response(exception,status = status.HTTP_404_NOT_FOUND)
                tour.delete()
                return Response(data={'message':'successfully deleted'},status=status.HTTP_200_OK)
            else:
                return Response(data={'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'message':'Not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
                

