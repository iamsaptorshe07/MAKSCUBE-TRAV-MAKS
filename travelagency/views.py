from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from django.http import *
from .tests import *
from django.contrib import messages
# Create your views here.
def travelagency_home(request,agid):
    return render(request,'travelagency/travelagent_home.html')

def addTour(request,uid,agid):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.id == uid and user.userAccess.agentId == agid:
            if request.method == 'POST':
                sdate = tourDate(request.POST.get('sdate'))
                print("\n\n",sdate,"\n\n")
                edate = tourDate(request.POST.get('edate'))
                print("\n\n",edate,"\n\n")
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
                messages.success(request,'Tour Added Successfully')
                return redirect('/travelagency/agencytours/{}/{}'.format(user.id,user.userAccess.agentId))
            else:
                return HttpResponse("BAD REQUEST")
        else:
            return HttpResponse("BAD REQUEST")
    else:
        return HttpResponse("BAD REQUEST")


def agencyTours(request,uid,agid):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.id == uid and user.userAccess.agentId == agid:
            if request.method == 'POST':
                pass
            else:
                tour = Tour.objects.filter(seller__userAccess__agentId = agid)
                for i in tour:
                    print(i.endLocation)
                print(tour)
                context = {
                    'Tours':tour,
                }
                return render(request,'travelagency/agency_tours.html',context=context)
        else:
            return HttpResponse("BAD REQUEST")
    else:
        return HttpResponse("BAD REQUEST")


def editTours(request,agentId,tourId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            if Tour.objects.filter(tourId=tourId,seller=user).exists():
                tour = Tour.objects.get(tourId=tourId)
                if request.method == 'POST':
                    pass
                    #Samiran complete this function
                else:
                    #Samiran complete/restructure it 
                    context = {
                        'Tour':tour
                    }
                    return render(request,'travelagency/edit_tours.html',context=context)
            else:
                return HttpResponse("BAD REQUEST")
        else:
            return HttpResponse("404 forbidden")
    else:
        return HttpResponse("404 forbidden")



def deleteteTour(request,agentId,tourId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            if Tour.objects.filter(tourId=tourId,seller=user).exists():
                tour = Tour.objects.get(tourId=tourId)
                tour.delete()
                messages.success(request,'Tou deleted succesfully')
                return redirect('/travelagency/agencytours/{}/{}'.format(user.id,user.userAccess.agentId)')
            else:
                return HttpResponse('BAD REQUEST')
        else:
            return HttpResponse('404 ERROR')
    return HttpResponse('404 ERROR')




