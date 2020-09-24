from django.shortcuts import render,redirect
from accounts.models import *
from touring.models import *
from travelagency.models import *
from django.http import *
from django.contrib import messages
# Create your views here.

def bookingHistory(request,userId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='traveller':
        if user.userAccess.userId == userId:
            bookings = Order.objects.filter(customer=user)
            context = {
                'Bookings':bookings
            }
            return render(request,'traveller/bookingtour_history.html',context=context)
        else:
            return HttpResponse('BAD REQUEST')
    else:
        return HttpResponse("BAD REQUEST")
