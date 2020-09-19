from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from django.http import *
from .tests import *
# Create your views here.
def travelagency_home(request,agid):
    return render(request,'travelagency/travelagent_home.html')

def addTour(request,uid,agid):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if request.method == 'POST':
            sdate = tourDate(request.POST.get('sdate'))
            print("\n\n",sdate,"\n\n")
            edate = tourDate(request.POST.get('edate'))
            print("\n\n",edate,"\n\n")
            slocation = request.POST.get('slocstate')+"**"+request.POST.get('sloccity')
            elocation = request.POST.get('elocstate')+"**"+request.POST.get('eloccity')
            price = request.POST.get('price')
            ttype = request.POST.get('ttype')
            thumbnail = request.FILES.get('thumbnail')
            ttitle = request.POST.get('ttitle')
            inclusive = request.POST.get('inclusive')
            exclusive = request.POST.get('exclusive')
            highlight = request.POST.get('highlight')
            overview = request.POST.get('overview')
            duration = tourDuration(request.POST.get('sdate'),request.POST.get('edate'))+2
            tourId = tourIdMaker()
            print('\n\n',tourId,'\n\n')
            description_dct = {}
            for i in range(duration):
                description_dct['day{}'.format(i+1)]=[request.POST.get('dayTitle{}'.format(i+1)),request.POST.get('dayDescription{}'.format(i+1))]
            print(description_dct)
            slug = ''
            for character in ttitle:
                if character.isalnum():
                    slug+=character
            slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
                slocation,elocation,sdate,agid,uid,tourId,ttype
            )
            print('\n\n',slug,'\n\n')
            description = descriptionMaker(description_dct)
            
            tour = Tour(
                #assign the values
                seller = user,
                agency = user.userAgency,
                tourSlug = slug,
                tourId = tourId,
                tourHeading = ttitle,
                startingLocation = slocation,
                endLocation = elocation,
                startDate = sdate,
                endDate = edate,
                description = description,
                inclusive = inclusive,
                exclusive = exclusive,
                highlight = highlight,
                price = price,
                tour_type = ttype,
                thumbnail = thumbnail,
                
            )
            tour.save()
            return HttpResponse("TOUR IS ADDED")
        else:
            return render(request,'travelagency/travelagent_home.html')
    else:
        return HttpResponse("BAD REQUEST")