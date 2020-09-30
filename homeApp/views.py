from django.shortcuts import render, redirect
from django.http import *
from travelagency.models import *

# Homepage Function
def index(request):
    tour = Tour.objects.all()
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

