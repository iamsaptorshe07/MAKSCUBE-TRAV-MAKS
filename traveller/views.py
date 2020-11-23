from django.shortcuts import render,redirect
from accounts.models import *
from touring.models import *
from invoice.invoice_generator import render_to_pdf
from travelagency.models import *
from django.http import *
from django.contrib import messages
from datetime import date
# Create your views here.


def bookingHistory(request):
    user = request.user
    if request.method=='GET':
        if user.is_authenticated and request.session['access_type']=='traveller':
            bookings = Order.objects.filter(customer=user).order_by('-id')
            context = {
                'Bookings':bookings
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

def ongoingTour(request):
    return render(request,'traveller/ongoing_tour.html')

def upcomingTour(request):
    return render(request,'traveller/upcoming_tour.html')