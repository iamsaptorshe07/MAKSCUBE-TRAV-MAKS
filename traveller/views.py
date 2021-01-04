from django.shortcuts import render,redirect
from accounts.models import *
from touring.models import *
from invoice.invoice_generator import render_to_pdf
from travelagency.models import *
from django.http import *
from django.contrib import messages
from datetime import date
from .models import WishList
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def bookingHistory(request):
    user = request.user
    if request.method=='GET':
        if user.is_authenticated and request.session['access_type']=='traveller':
            bookings = Order.objects.filter(customer=user).order_by('-id')
            context = {
                'Bookings':bookings,

            }
            return render(request,'traveller/bookingtour_history.html',context=context)
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

def invoiceGenerator(request,orderID):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='traveller':
        if Payment.objects.filter(Order__order_id=orderID,Order__customer=user).exists():
            invoice = Payment.objects.get(Order__order_id=orderID,Order__customer=user)
            bill_context = {
                "transactionId": invoice.transaction_id,
                "bankTransactionId": invoice.banktransaction_id,
                "orderId": invoice.Order.order_id,
                "date": invoice.txn_date,
                "CMail": invoice.Order.customer_email,
                "CPhone": invoice.Order.customer_phone,
                "CName": invoice.Order.customer_name,
                "CAddress": invoice.Order.customer_address,
                "tourId": invoice.Order.tour.tourId,
                "startdate": invoice.Order.tour.startDate,
                "endDate": invoice.Order.tour.endDate,
                "startLocation": invoice.Order.tour.startingLocation,
                "endLoaction": invoice.Order.tour.endLocation,
                "placedBy": invoice.Order.customer.userAccess.userId,
                "Quentity": invoice.Order.total_people,
                "price":invoice.Order.paid_by_user,
                "total_price":invoice.Order.total_price,
                "To_be_paid":invoice.Order.total_price - invoice.Order.paid_by_user,
                'orderDate': invoice.creation_date,
                "agentId": invoice.Order.agent.userAccess.agentId,
                "AgencyId": invoice.Order.agency.agency_Id,
                'ppp': invoice.Order.tour.price,
                'total_people':invoice.Order.total_people

            }
            pdf = render_to_pdf('invoice/bill.html', bill_context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "{}.pdf".format(invoice.Order.order_id)
                content = "inline; filename={}".format(filename)
                response['Content-Disposition'] = content
                return response
            else:
                return HttpResponse("Internal Problem Occured")
        else:
            return render(request,'forbidden.html')

    else:
        return render(request,'forbidden.html')

def ongoingTour(request,userId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='traveller':
        if user.userAccess.userId == userId:
            tours = Order.objects.filter(customer=user)
            Tour=[]
            for i in tours:
                if i.tour.startDate < date.today() and date.today() < i.tour.endDate :
                    Tour.append(i)
            context = {
                'Tours':Tour,
                'uid':userId,
                'len':len(Tour),
            }
            return render(request,'traveller/ongoing_tour.html',context=context)
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

def upcomingTour(request,userId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='traveller':
        if user.userAccess.userId == userId:
            tours = Order.objects.filter(customer=user)
            Tour=[]
            for i in tours:
                print(i)
                if i.tour.startDate > date.today():
                    Tour.append(i)
            context = {
                'Tours':Tour,
                'uid':userId,
                'len':len(Tour),
            }
            return render(request,'traveller/upcoming_tour.html',context=context)
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

@csrf_exempt
def wishList(request):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='traveller':
        if request.method == 'POST':
            tour = request.POST.get('post_id')
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
            return HttpResponse("Success!")
        else:
            wishlist = WishList.objects.filter(user=user)
            context = {
                'Wishlist':wishlist,
            }
            for i in wishlist:
                print(i.tour.price)
            return render(request,'traveller/wishlist.html',context=context)
    else:
        return render(request,'forbidden.html')


def writeReview(request,tourId):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated and request.session['access_type']=='traveller':
            if Tour.objects.filter(tourId=tourId).exists():
                tour = Tour.objects.get(tourId=tourId)
                rating = int(request.POST.get('rating'))
                comment = request.POST.get('comment')
                if rating>5:
                    rating = 5
                elif rating<0:
                    rating = 1
                review = Review(
                    tour = tour,
                    user = user,
                    rating = rating,
                    comment = comment 
                )
                review.save()
                messages.success(request,'Recieved Your Rating Thank You')
                return redirect('bookingHistory')
            else:
                return render(request,'forbidden.html')
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

