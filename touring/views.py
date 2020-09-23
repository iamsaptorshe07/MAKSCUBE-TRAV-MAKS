from django.shortcuts import render, redirect
from django.http import *
from .models import *
from accounts.models import  *
from travelagency.models import *
from.tests import *
from django.contrib import messages
from .tests import *
from paytm import Checksum
import requests
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def searchTour(request):
    slocation = request.GET.get('sLocation')
    elocation = request.GET.get('eLocation')
    sDate = request.GET.get('sDate')
    tours = Tour.objects.filter(startingLocation__icontains=slocation,endLocation__icontains=elocation,startDate=sDate)
    context = {
        'Tours':tours,
    }
    return render(request,'touring/tour_search.html',context=context)

def advancedSearching(request):
    pass

def tourDetails(request,tourId,slug):
    if(Tour.objects.filter(tourSlug=slug).exists()):
        tour = Tour.objects.get(tourSlug=slug)
        context = {
            'Tour':tour
        }
        return render(request,'touring/tour_details.html',context=context)
    else:
        return HttpResponse("BAD REQUEST")


def bookTour(request,tourId,agentId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='traveller':
        if Tour.objects.filter(tourId=tourId).exists() and AccountType.objects.filter(agentId=agentId).exists():
            seller_account = AccountType.objects.get(agentId=agentId)
            if Tour.objects.filter(tourId=tourId,seller=seller_account.user).exists():
                tour = Tour.objects.get(tourId=tourId,seller=seller_account.user)
                if request.method == 'POST':
                    name = request.POST.get('name')
                    email = request.POST.get('email')
                    phone = request.POST.get('phone')
                    address = request.POST.get('address')
                    total_people = int(request.POST.get('total_people'))
                    payment = tour.price * total_people
                    order_id = OrderIdGenerator()
                    order = Order(
                        order_id = order_id,
                        customer = user,
                        customer_email = email,
                        customer_phone = phone,
                        customer_address = address,
                        total_people = total_people,
                        customer_name = name,
                        agent = tour.seller,
                        agency = tour.seller.userAgency,
                        payment_price = payment,
                        tour = tour,
                    )
                    order.save()
                    print(order.payment_price)
                    print(str(order.payment_price))
                    print(type(order.order_id))
                    print(order.customer.userAccess.userId)
                    print(type(order.customer.userAccess.userId))
                    MID = 'MjGguD53343847273362'
                    MKEY='3KD6MeB%t&QDio!7'
                    paytmParams = {
                        "MID" : MID,
                        "WEBSITE" : "WEBSTAGING",
                        "INDUSTRY_TYPE_ID" : "Retail",
                        "CHANNEL_ID" : "WEB",
                        "ORDER_ID" : order.order_id,
                        "CUST_ID" : order.customer.userAccess.userId,
                        "MOBILE_NO" : order.customer_phone,
                        "EMAIL" : order.customer_email,
                        "TXN_AMOUNT" : str(order.payment_price),
                        "CALLBACK_URL" : "http://127.0.0.1:8000/tour/paytm-payment-recieve",
                    }
                    checksum = Checksum.generateSignature(paytmParams, MKEY)
                    paytmParams['CHECKSUMHASH']= checksum
                    print(paytmParams)
                    return render(request,'paytm/paytm.html',{'data':paytmParams})
                else:
                    return render(request,'touring/tour_checkout.html',context={'Tour':tour})
            else:
                return HttpResponse("NO SUCH TOUR")
        else:
            return HttpResponse("BAD REQUEST")
    else:
        messages.warning(request,'Please Log in to book the tour')
        return redirect('traveler_accounts_signup')

@csrf_exempt
def recievePayment(request):
    MID = 'MjGguD53343847273362'
    MKEY='3KD6MeB%t&QDio!7'
    if request.method == 'POST':
        form = request.POST
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]
        isVerifySignature = Checksum.verifySignature(response_dict, MKEY, checksum)
        order = Order.objects.get(order_id = response_dict['ORDERID'])
        if isVerifySignature == True and order.payment_price == float(response_dict['TXNAMOUNT']):
            confirm_order = Payment(
                Order = order,
                transaction_id=response_dict['TXNID'],
                banktransaction_id = response_dict['BANKTXNID'],
                txn_date = response_dict['TXNDATE'],
                gateway_name = response_dict['GATEWAYNAME'],
                bankname = response_dict['BANKNAME'],
                payment_mode = response_dict['PAYMENTMODE'],
            )
            confirm_order.save()
            order.status = True
            order.save()
            # Kuntalda start your
            return HttpResponse("Genearating you bill")
        else:
            failed_order = Failed_Order(
                order_id=order.order_id,
                customer = order.customer,
                customer_email = order.customer_email,
                customer_phone = order.customer_phone,
                customer_name = order.customer_name,
                customer_address = order.customer_address,
                agent = order.agent,
                agency=order.agency,
                tour=order.tour,
                creation_time = order.creation_time,
                payment_price = order.payment_price,
                total_people=order.total_people
            )
            failed_order.save()
            order.delete()
            return HttpResponse("Some Problem Occured, if you have lost your money contact us")
    else:
        return HttpResponse("not allowed")
