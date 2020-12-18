from django.shortcuts import render, redirect
from django.http import *
from travelagency.models import *
import datetime
from django.db.models import Q
# Homepage Function
def index(request):
    tour = Tour.objects.filter(publish_mode=True,last_booking_date__gte=str(datetime.date.today()),maximum_people__gte=1)
    context = {'Tour' : tour}
    return render(request,'home.html', context=context)

def aboutUs(request):
    return render(request,'home_app/aboutus.html')

def contactUs(request):
    return render(request,'home_app/contactus.html')

def userPrivacyPolicy(request):
    return render(request,'home_app/userprivacypolicy.html')

def userFAQ(request):
    return render(request,'home_app/userFAQ.html')

def termsAndCondition(request):
    return render(request,'home_app/termsandcondition.html')

def partnerBenifits(request):
    return render(request,'home_app/partnerbenifits.html')

def partnerBenifitsTavellers(request):
    return render(request,'home_app/partnerbenifitstravellers.html')

def partnerFAQ(request):
    return render(request,'home_app/partnerfaq.html')

def userPaymentPolicy(request):
    return render(request,'home_app/userpaymentpolicy.html')

def downloadApp(request):
    return render(request,'home_app/downloadapp.html')

def betaMode(request):
    return render(request,'beta.html')
