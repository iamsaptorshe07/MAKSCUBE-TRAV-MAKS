from django.shortcuts import render
from .models import *
# Create your views here.
def travelagency_home(request,uid,agid):
    return render(request,'travelagency/travelagent_home.html')
