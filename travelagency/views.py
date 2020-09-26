from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from django.http import *
from .tests import *
from django.contrib import messages

# Create your views here.
def travelagency_home(request,agid):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agid:
            if request.method == 'GET':
                return render(request,'travelagency/travelagent_home.html')
            else:
                return HttpResponse("BAD REQUEST")
        else:
            return HttpResponse("BAD REQUEST")
    else:
        return HttpResponse("BAD REQUEST")

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
                maximum_people = request.POST.get('seat')
                ttype = request.POST.get('ttype')
                thumbnail = request.FILES.get('thumbnail')
                ttitle = request.POST.get('ttitle')
                inclusive = request.POST.get('inclusive')
                exclusive = request.POST.get('exclusive')
                highlight = request.POST.get('highlight')
                overview = request.POST.get('overview')
                duration = tourDuration(request.POST.get('sdate'),request.POST.get('edate'))+1
                tourId = tourIdMaker()
                print('\n\n',tourId,'\n\n')
                description_dct = {}
                for i in range(duration):
                    description_dct['dayTitle{}'.format(i+1)]=str(request.POST.get('dayTitle{}'.format(i+1))).strip()
                    print(request.POST.get('dayDescription{}'.format(i+1)))
                    description_dct['dayDescription{}'.format(i+1)]=str(request.POST.get('dayDescription{}'.format(i+1))).strip()
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
                    tourId = tourId,
                    tourSlug = slug.strip(),
                    tourHeading = ttitle.strip(),
                    startingLocation = slocation.strip(),
                    endLocation = elocation.strip(),
                    startDate = sdate.strip(),
                    endDate = edate.strip(),
                    description = description.strip(),
                    inclusive = inclusive.strip(),
                    exclusive = exclusive.strip(),
                    highlight = highlight.strip(),
                    price = price.strip(),
                    tour_type = ttype.strip(),
                    thumbnail = thumbnail,
                    overview = overview.strip(),
                    maximum_people = maximum_people.strip(),
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
            if request.method == 'GET':
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
    else:
        return HttpResponse("BAD REQUEST")


def editTours(request,agentId,tourId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            if Tour.objects.filter(tourId=tourId,seller=user).exists():
                tour = Tour.objects.get(tourId=tourId)
                if tour.publish_mode:
                    return redirect('/')
                else:
                    if request.method == 'POST':
                        sdate = tourDate(request.POST.get('sdate'))
                        if request.POST.get('edate') is not None:
                            print("\n\nEdate",request.POST.get('edate'),"\n\n")
                            if tour.endDate != request.POST.get('edate'):
                                edate = tourDate(request.POST.get('edate'))
                                print("\n\n",edate,"\n\n")
                        slocation = request.POST.get('slocation')
                        elocation = request.POST.get('elocation')
                        price = request.POST.get('price')
                        ttype = request.POST.get('ttype')
                        
                        ttitle = request.POST.get('ttitle')
                        inclusive = request.POST.get('inclusive')
                        exclusive = request.POST.get('exclusive')
                        highlight = request.POST.get('highlight')
                        overview = request.POST.get('overview')
                        maximum_people = request.POST.get('seat')
                        if tour.endDate != request.POST.get('edate'):
                            duration = tourDuration(request.POST.get('sdate'),request.POST.get('edate'))+1
                        else:
                            duration = tourDuration(request.POST.get('sdate'),request.POST.get('edate'))+1

                        description_dct = {}
                        for i in range(duration):
                            description_dct['dayTitle{}'.format(i+1)]=request.POST.get('dayTitle{}'.format(i+1)).strip()
                            description_dct['dayDescription{}'.format(i+1)]=request.POST.get('dayDescription{}'.format(i+1)).strip()
                            print(description_dct)
                        slug = ''
                        for character in ttitle:
                            if character.isalnum():
                                slug+=character
                        slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
                            slocation,elocation,sdate,agentId,user.id,tourId,ttype
                        )
                        print('\n\n',slug,'\n\n')
                        description = descriptionMaker(description_dct)
                        tour.tourHeading = ttitle.strip()
                        tour.tourSlug = slug.strip()
                        tour.startingLocation = slocation.strip()
                        tour.endLocation = elocation.strip()
                        tour.endDate = edate.strip()
                        tour.description = description.strip()
                        tour.inclusive = inclusive.strip()
                        tour.exclusive = exclusive.strip()
                        tour.highlight = highlight.strip()
                        tour.price = price.strip()
                        tour.tour_type = ttype
                        if request.FILES.get('thumbnail') is not None:
                            tour.thumbnail = request.FILES.get('thumbnail')
                        tour.overview = overview.strip()
                        tour.maximum_people = maximum_people

                        tour.save()
                        messages.success(request,'Successfully Updated')
                        return redirect('/travelagency/agencytours/{}/{}'.format(user.id,user.userAccess.agentId))
                        
                    else:
                        #Samiran complete/restructure it 
                        desc = tour.description.strip('TRAVMAKS')
                        print("\n\n",desc)
                        context = {
                            'Tour':tour,
                            'desc': desc,
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
                return redirect('/travelagency/agencytours/{}/{}'.format(user.id,user.userAccess.agentId))
            else:
                return HttpResponse('BAD REQUEST')
        else:
            return HttpResponse('404 ERROR')
    return HttpResponse('404 ERROR')




