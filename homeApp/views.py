from django.shortcuts import render, redirect
from django.http import *
from travelagency.models import *

# Homepage Function
def index(request):

    tour = Tour.objects.all()
    context = {'Tour' : tour}
    return render(request,'home.html', context=context)
