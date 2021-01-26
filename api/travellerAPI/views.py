from django.shortcuts import render
from datetime import date
from touring.models import Order,Cancelled_Order
from api.tours.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.contrib.sites.shortcuts import get_current_site
from traveller.models import WishList
from .serializers import WishListSerializer
from travelagency.models import Tour
# Create your views here.
class UpcomingTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='traveller':
                upcomingTour = Order.objects.filter(customer = request.user,status=True,agent_approval=True)
                orders = []
                for i in upcomingTour:
                    if i.tour.startDate > date.today():
                        orders.append(i)
                order_serializer = OrderSerializer(orders,many=True)
                return Response(
                    data = {
                        'status':200,
                        'upcomingTours':order_serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

class OngoingTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='traveller':
                ongoingTour= Order.objects.filter(customer = request.user,status=True,agent_approval=True)
                orders = []
                for i in ongoingTour:
                    if date.today() >= i.tour.startDate and date.today() <= i.tour.endDate:
                        orders.append(i)
                order_serializer = OrderSerializer(orders,many=True)
                return Response(
                    data = {
                        'status':200,
                        'ongoingTours':order_serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )


class MyBookingHistory(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='traveller':
                success_history = Order.objects.filter(customer=request.user,status=True,agent_approval=True)
                cancel_history = Cancelled_Order.filter(customer=request.user,status=True,agent_approval=True)
                order_history = success_history.union(cancel_history).order_by('-creation_date')
                order_serializer = OrderSerializer(order_history,many=True)
                return Response(
                    data = {
                        'status':200,
                        'orderHistory':order_serializer.data
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )



class WishListAPI(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            user = request.user
            if request.session['access_type']=='traveller':
                wishlist = WishList.objects.filter(user=user)
                wishlist= WishListSerializer(wishlist,many=True)
                data = wishlist.data
                print(data)
                for i in data:
                    site = str(get_current_site(request))
                    tour = Tour.objects.get(id=i['tour'])
                    i['tour_name']=tour.tourHeading
                    i['tour_thumbnail']=site + tour.thumbnail.url
                    i['tour_slug']=tour.tourSlug
                return Response(
                    data = {
                    'status':200,
                    'wishlist':wishlist.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )
    
    def post(self,request):
        if request.session.session_key:
            if request.session['access_type']=='traveller':
                tour = request.POST.get('tourId')
                tour = Tour.objects.get(tourId=tour)
                if WishList.objects.filter(tour=tour,user=user).exists():
                    wishlist = WishList.objects.get(tour=tour,user=user)
                    wishlist.delete()
                else:
                    wishlist = WishList(
                        tour = tour,
                        user = user,
                    )
                    wishlist.save()
                return Response(
                    data = {
                    'status':200,
                    'message':"Success!"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data = {
                        'status':401,
                        'message':"Not Authorized"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data = {
                    'status':404,
                    'message':"Not Authenticated"
                },
                status = status.HTTP_400_BAD_REQUEST
            )


