from django.shortcuts import render, redirect
from django.http import *
from .models import *
from accounts.models import  *
from.tests import *
from django.contrib import messages
# Create your views here.

def searchTour(request):
    return render(request,'touring/tour_search.html')

def tourDetails(request):
    return render(request,'touring/tour_details.html')
