from django.shortcuts import render, redirect
from django.http import *
from .models import *
from accounts.models import  *
from travelagency.models import *
from.tests import *
from django.contrib import messages
# Create your views here.

def searchTour(request):
    slocation = request.GET.get('sLocation')
    elocation = request.GET.get('eLocation')
    sDate = request.GET.get('sDate')
    tours = Tour.objects.filter(startingLocation__icontains=slocation,endLocation__icontains=elocation,startDate=sDate)
    context = {
        'Tours':tours,
    }
    return render(request,'touring/tour_search.html')

def advancedSearching(request):
    pass

def tourDetails(request):
    return render(request,'touring/tour_details.html')

