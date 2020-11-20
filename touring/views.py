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
#import json
from django.views.decorators.csrf import csrf_exempt
from invoice.invoice_generator import render_to_pdf
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

def searchTour(request):
    slocation = request.GET.get('sLocation')
    elocation = request.GET.get('eLocation')
    tours = Tour.objects.filter(startingLocation__icontains=slocation,endLocation__icontains=elocation)
    context = {
        'Tours':tours,
    }
    return render(request,'touring/tour_search.html',context=context)

def advancedSearching(request):
    pass

def tourDetails(request,tourId,slug):
    if(Tour.objects.filter(tourSlug=slug).exists()):
        tour = Tour.objects.get(tourSlug=slug)
        d=tour.description
        
        tourImage = TourImage.objects.get(tour=tour)
        images=[]
        try:
            images.append(tourImage.image1.url)
        except:
            pass
        try:
            images.append(tourImage.image2.url)
        except:
            pass
        try:
            images.append(tourImage.image3.url)
        except:
            pass
        try:
            images.append(tourImage.image4.url)
        except:
            pass
        try:
            images.append(tourImage.image5.url)
        except:
            pass
        try:
            images.append(tourImage.image6.url)
        except:
            pass
        context = {
            'Tour':tour,
            'description': d,
            'images' : images,
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
                        "CALLBACK_URL" : "http://{}/tour/paytm-payment-recieve".format(get_current_site(request)),
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
        return redirect('Traveller_Login')

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
            bill_context = {
                "transactionId" : confirm_order.transaction_id,
                "bankTransactionId" : confirm_order.banktransaction_id,
                "orderId" : confirm_order.Order.order_id,
                "date" : response_dict['TXNDATE'] ,
                "CMail" : confirm_order.Order.customer_email,
                "CPhone" : confirm_order.Order.customer_phone,
                "CName" : confirm_order.Order.customer_name,
                "CAddress" : confirm_order.Order.customer_address,
                "tourId" : confirm_order.Order.tour.tourId,
                "startdate" : confirm_order.Order.tour.startDate,
                "endDate" : confirm_order.Order.tour.endDate,
                "startLocation" : confirm_order.Order.tour.startingLocation,
                "endLoaction" : confirm_order.Order.tour.endLocation,
                "placedBy" : confirm_order.Order.customer.userAccess.userId,
                "Quentity" : confirm_order.Order.total_people,
                "price":confirm_order.Order.payment_price,
                'orderDate':confirm_order.creation_date,
                "agentId":confirm_order.Order.agent.userAccess.agentId,
                "AgencyId":confirm_order.Order.agency.agency_Id,
                'ppp':confirm_order.Order.tour.price

            }
            pdf = render_to_pdf('invoice/bill.html',bill_context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "{}.pdf".format(confirm_order.Order.order_id)
                content = "inline; filename={}".format(filename)
                response['Content-Disposition'] = content
                return response
            else:
                return HttpResponse("Problem Occured")
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
                creation_date = order.creation_date,
                payment_price = order.payment_price,
                total_people=order.total_people
            )
            failed_order.save()
            order.delete()
            return HttpResponse("Some Problem Occured, if you have lost your money contact us")
    else:
        return HttpResponse("not allowed")
