from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from django.http import *
from .tests import *
from django.contrib import messages
from touring.models import *

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
                description_dct = ""
                for i in range(duration):
                    for i in range(duration):
                        description_dct=description_dct+str(request.POST.get('dayTitle{}'.format(i+1))).strip()+"$$$$"+str(request.POST.get('dayDescription{}'.format(i+1))).strip()+"@@@@"
 
                    #description_dct['dayTitle{}'.format(i+1)]=str(request.POST.get('dayTitle{}'.format(i+1))).strip()
                    #print(request.POST.get('dayDescription{}'.format(i+1)))
                    #description_dct['dayDescription{}'.format(i+1)]=str(request.POST.get('dayDescription{}'.format(i+1))).strip()
                print(description_dct)
                slug = ''
                for character in ttitle:
                    if character.isalnum():
                        slug+=character
                slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
                    slocation,elocation,sdate,agid,uid,tourId,ttype
                )
                print('\n\n',slug,'\n\n')
                description = description_dct.strip('@@@@')
                last_booking_date = tourDate(request.POST.get('bookinglimit'))
                last_cancel_date = tourDate(request.POST.get('cancelllimit'))
                print(last_booking_date,"\n\n",last_cancel_date,"\n\n")
                
                
                tour = Tour(
                    #assign the values
                    seller = user,
                    agency = user.userAgency,
                    tourId = tourId,
                    tourSlug = slug.strip(),
                    tourHeading = ttitle.strip(),
                    startingLocation = slocation.strip(),
                    endLocation = elocation.strip(),
                    startDate = sdate,
                    endDate = edate,
                    description = description.strip(),
                    inclusive = inclusive.strip(),
                    exclusive = exclusive.strip(),
                    highlight = highlight.strip(),
                    price = price.strip(),
                    tour_type = ttype.strip(),
                    thumbnail = thumbnail,
                    overview = overview.strip(),
                    maximum_people = maximum_people.strip(),
                    last_booking_date = last_booking_date,
                    last_cancel_date = last_cancel_date
                )
                tour.save()

                image1 = request.FILES.get('image1')
                image2 = request.FILES.get('image2')
                image3 = request.FILES.get('image3')
                image4 = request.FILES.get('image4')
                image5 = request.FILES.get('image5')
                image6 = request.FILES.get('image6')

                tourImage = TourImage(
                        tour = tour,
                        image1 = image1,
                        image2 = image2,
                        image3 = image3,
                        image4 = image4,
                        image5 = image5,
                        image6 = image6

                )

                tourImage.save()


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

                        description_dct = ""
                        for i in range(duration):
                            description_dct=description_dct+str(request.POST.get('dayTitle{}'.format(i+1))).strip()+"$$$$"+str(request.POST.get('dayDescription{}'.format(i+1))).strip()+"@@@@"
 
                        #for i in range(duration):
                            #description_dct['dayTitle{}'.format(i+1)]=request.POST.get('dayTitle{}'.format(i+1)).strip()
                            #description_dct['dayDescription{}'.format(i+1)]=request.POST.get('dayDescription{}'.format(i+1)).strip()
                        print(description_dct)
                        slug = ''
                        for character in ttitle:
                            if character.isalnum():
                                slug+=character
                        slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
                            slocation,elocation,sdate,agentId,user.id,tourId,ttype
                        )
                        print('\n\n',slug,'\n\n')
                        description = description_dct.strip('@@@@')
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
                        image1 = request.FILES.get('image1')
                        image2 = request.FILES.get('image2')
                        image3 = request.FILES.get('image3')
                        image4 = request.FILES.get('image4')
                        image5 = request.FILES.get('image5')
                        image6 = request.FILES.get('image6')

                        tourImage = TourImage.objects.get(tour=tour)
                        if image1 is not None:
                            tourImage.image1 = image1
                        if image2 is not None:
                            tourImage.image2 = image2
                        if image3 is not None:
                            tourImage.image3 = image3
                        if image4 is not None:
                            tourImage.image4 = image4
                        if image5 is not None:
                            tourImage.image5 = image5
                        if image6 is not None:
                            tourImage.image6 = image6
                        tourImage.save()
                        messages.success(request,'Successfully Updated')
                        return redirect('/travelagency/agencytours/{}/{}'.format(user.id,user.userAccess.agentId))
                        
                    else:
                        
                        desc = tour.description
                        tourImage=TourImage.objects.get(tour=tour)


                        print("\n\n",desc)
                        context = {
                            'Tour':tour,
                            'desc': desc,
                            'tourImage':tourImage,
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
                if tour.publish_mode:
                    messages.success(request,"Tour is already published you can't deleted tour! Please contact us!")
                    return redirect('/travelagency/agencytours/{}/{}'.format(user.id,user.userAccess.agentId))
                else:
                    tour.delete()
                    messages.success(request,'Tour deleted succesfully')
                    return redirect('/travelagency/agencytours/{}/{}'.format(user.id,user.userAccess.agentId))
            else:
                return HttpResponse('BAD REQUEST')
        else:
            return HttpResponse('404 ERROR')
    return HttpResponse('404 ERROR')



def booking_history(request,agentId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            tours = Order.objects.filter(agent=user)
            context = {
                'Tours':tours
            }
            return render(request,'travelagency/booking_history.html',context=context)
        else:
            return HttpResponse("BAD Request")
    else:
        return HttpResponse("Not have the permission")


def upcoming_tours(request,agentId):
      return render(request,'travelagency/upcoming_tours.html')

def ongoing_tours(request,agentId):
      return render(request,'travelagency/ongoing_tours.html')



