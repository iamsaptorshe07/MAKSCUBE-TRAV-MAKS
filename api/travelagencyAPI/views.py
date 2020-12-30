from django.shortcuts import render
from datetime import date
from travelagency.models import Tour, TourImage
from touring.models import Order,Cancelled_Order
from .serializers import TourSerializer, TourImageSerializer
from api.tours.serializers import OrderSerializer
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
                date_gap = date.today() - tour.creationDate
                if date_gap.days > 2:
                    return Response(
                        data={
                            'status':401,
                            'message':'You are not authorized to delete the tour anymore'
                            },
                        status=status.HTTP_401_UNAUTHORIZED
                        )
                tour.delete()
                return Response(data={'message':'successfully deleted'},status=status.HTTP_200_OK)
            else:
                return Response(data={'message':'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'message':'Not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
                

class OngoingTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                ongoingTour = Order.objects.filter(agent=request.user,status=True,agent_approval=True)
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
        
# Order Accept or Decline API
class AcceptOrDeclineTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def put(self,request,orderId):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                if Order.objects.filter(order_id = orderId,agent = request.user).exists():
                    order = Order.object.get(order_id = orderId)
                    agent_approval = request.data
                    if agent_approval['approval']==True:
                        order.agent_approval = True
                        return Response(
                            data = {
                                'status':200,
                                'message':"Congratualations! We are glad that you get booking through us"
                            },
                            status = status.HTTP_200_OK
                        )
                    elif agent_approval['approval'] == False:
                        cancelled_order = Cancelled_Order(
                            order_id = order.order_id,
                            tour = order.tour,
                            customer = order.customer,
                            customer_name = order.customer_name,
                            customer_email = order.customer_email,
                            customer_phone = order.customer_phone,
                            customer_address = order.customer_address,
                            agent = order.agent,
                            agency = order.agency,
                            total_people = order.total_people,
                            paid_by_user = order.paid_by_user,
                            total_price = order.total_price,
                            creation_date = order.creation_date,
                            cancelled_by = "AGENT",
                        )
                        cancelled_order.save()
                        tour = order.tour
                        tour.maximum_people+=order.total_people
                        tour.save()
                        order.delete()
                        return Response(
                            data = {
                                'status':200,
                                'mesaage':"Our Executives will call you please provide us a valid reason for not accepting the offer"
                            },
                            status = status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            data={
                                'status':406,
                                'message':"Send either true or false, only boolean value is allowed"
                            },
                            status = status.HTTP_406_NOT_ACCEPTABLE 
                            )
                else:
                    return Response(
                            data={
                                'status':404,
                                'message':"Order Not Found!"
                            },
                            status = status.HTTP_404_NOT_FOUND
                            )
            else:
                return Response(
                            data={
                                'status':401,
                                'message':"Not Authorized!"
                            }, 
                            status = status.HTTP_401_UNAUTHORIZED
                            )
        else:
            return Response(
                            data = {
                                'status':400,
                                'message':"Not Authenticated!"
                            },
                            status = status.HTTP_400_BAD_REQUEST
                            )

                    


class IncomingOrderStack(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                order = Order.objects.filter(agent=request.user,status=True,agent_approval=False)
                order_data = OrderSerializer(order,many=True)
                return Response(
                            data = {
                                'status':200,
                                'incoming_orders':order_data.data
                            },
                            status = status.HTTP_200_OK
                            )
            else:
                return Response(
                            data={
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


class UpcomingTour(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                upcomingTour = Order.objects.filter(agent=request.user,status=True,agent_approval=True)
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


class OrderBookingHistory(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                success_history = Order.objects.filter(agent=request.user,status=True,agent_approval=True)
                cancel_history = Cancelled_Order.filter(agent=request.user,status=True,agent_approval=True)
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






