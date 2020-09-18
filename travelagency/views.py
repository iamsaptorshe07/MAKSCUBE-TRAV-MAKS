from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from django.http import *
from .tests import *
# Create your views here.
def travelagency_home(request,agid):
    return render(request,'travelagency/travelagent_home.html')

def addTour(request,uid,agid):
    if user.is_authenticated() and request.session['access_type']=='seller':
        if request.method == 'POST':
            sdate = request.POST.get('sdate')
            edate = request.POST.get('edate')
            slocation = request.POST.get('slocation')
            elocation = request.POST.get('elocation')
            price = request.POST.get('price')
            ttype = request.POST.get('ttype')
            thumbnail = request.FILES.get('thumbnail')
            ttitle = request.POST.get('ttitle')
            inclusive = request.POST.get('inclusive')
            exclusive = request.POST.get('exclusive')
            highlight = request.POST.get('highlight')
            overview = request.POST.get('overview')
            duration = (edate - sdate)+2
            tourId = tourIdMaker()
            description_dct = {}
            for i in range(duration):
                description_dct['day{}'.format(i)]=[request.POST.get('dayTitle1'),request.POST.get('dayDescription1')]
            print(description_dct)
            slug = ''
            for character in ttitle:
                if character.isalnum():
                    slug+=character
            slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
                slocation,elocation,sdate,agid,uid,tourId,ttype
            )
            return HttpResponse("Okay")
        else:
            return render(request,'travelagency/travelagent_home.html')