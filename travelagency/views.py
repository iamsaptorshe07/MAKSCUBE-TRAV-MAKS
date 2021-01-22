from django.shortcuts import render,redirect
from accounts.models import *
from .models import *
from django.http import *
from .tests import *
from django.contrib import messages
from touring.models import *
from datetime import datetime 
from datetime import date

# Create your views here.
def travelagency_home(request,agid):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if AgencyDetail.objects.filter(user=user).exists():
            if user.userAccess.agentId == agid:
                if request.method == 'GET':
                    return render(request,'travelagency/travelagent_home.html')
                else:
                    return render(request,'forbidden.html')
            else:
                return render(request,'forbidden.html')
        else:
            messages.warning(request,'In order to add your tour, register your agency')
            return redirect('RegisterAgency')
    else:
        return render(request,'forbidden.html')

def addTour(request,uid,agid):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.id == uid and user.userAccess.agentId == agid:
            if request.method == 'POST':
                sdate = tourDate(request.POST.get('sdate'))
                print("\n\n",sdate,"\n\n")
                edate = tourDate(request.POST.get('edate'))
                print("\n\n",edate,"\n\n")

                special_tour_type=request.POST.get('additionalFeature')
                print("\n\nadditionalFeature--->>> ",special_tour_type,"\n\n")
                specialOffer = request.POST.get('spoffer')
                print("\n\nspecialOffer--->>> ",specialOffer,"\n\n")
                if specialOffer:
                    specialOfferDescription = str(request.POST.get('spofferdetails')).strip()
                    print("\n\nspecialOfferDescription--->>> ",specialOfferDescription,"\n\n")

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
                        description_dct=description_dct+str(request.POST.get('dayTitle{}'.format(i+1))).strip()+"$$$$"+str(request.POST.get('dayDescription{}'.format(i+1))).strip()+"@@@@"
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
                    special_tour_type = special_tour_type,
                    specialOffer = specialOffer,
                    specialOfferDescription = specialOfferDescription,
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
                return render(request,'forbidden.html')
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')


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
                return render(request,'forbidden.html')
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')


def editTours(request,agentId,tourId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            if Tour.objects.filter(tourId=tourId,seller=user).exists():
                tour = Tour.objects.get(tourId=tourId)
                if request.method == 'POST':
                    sdate = tourDate(request.POST.get('sdate'))
                    edate = tourDate(request.POST.get('edate'))
                    print("\n\n",edate,"\n\n")
                    slocation = request.POST.get('slocation')
                    elocation = request.POST.get('elocation')
                    price = request.POST.get('price')
                    ttype = request.POST.get('ttype')
                    
                    special_tour_type=request.POST.get('additionalFeature')
                    print("\n\nspecial_tour_type--->>> ",special_tour_type,"\n\n")
                    specialOffer = request.POST.get('spoffer')
                    print("\n\nspecialOffer--->>> ",specialOffer,"\n\n")
                    if specialOffer:
                        specialOfferDescription = str(request.POST.get('spofferdetails')).strip()
                        print("\n\nspecialOfferDescription--->>> ",specialOfferDescription,"\n\n")
                    
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
                    
                    last_booking_date = tourDate(request.POST.get('bookinglimit'))
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
                    tour.special_tour_type = special_tour_type
                    tour.specialOffer = specialOffer
                    if specialOffer:
                        tour.specialOfferDescription = specialOfferDescription
                    else:
                        tour.specialOfferDescription = None
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
                    ayan=0
                    desc = tour.description
                    print(desc)
                    tourImage=TourImage.objects.get(tour=tour)
                    immglist=[]
                    try:
                        immglist.append(tourImage.image1.url)
                        ayan+=1
                    except:
                        immglist.append('0')
                    try:
                        immglist.append(tourImage.image2.url)
                        ayan+=1
                    except:
                        immglist.append('0')
                    try:
                        immglist.append(tourImage.image3.url)
                        ayan+=1
                    except:
                        immglist.append('0')
                    try:
                        immglist.append(tourImage.image4.url)
                        ayan+=1
                    except:
                        immglist.append('0')
                    try:
                        immglist.append(tourImage.image5.url)
                        ayan+=1
                    except:
                        immglist.append('0')
                    try:
                        immglist.append(tourImage.image6.url)
                        ayan+=1
                    except:
                        immglist.append('0')

                    print("\n\n",desc)
                    context = {
                        'Tour':tour,
                        'desc': desc,
                        'publish':tour.publish_mode,
                        'imgLn':ayan,
                        'tourImage':tourImage,
                        # 'specialOffer':tour.specialOffer.strip(),
                        'imglist0':immglist[0],'imglist1':immglist[1],'imglist2':immglist[2],'imglist3':immglist[3],'imglist4':immglist[4],'imglist5':immglist[5],
                    }
                    
                    return render(request,'travelagency/edit_tours.html',context=context)
        
            else:
                return render(request,'forbidden.html')
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')



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
                return render(request,'forbidden.html')
        else:
            return render(request,'404.html')
    return render(request,'forbidden.html')

def booking_history(request,agentId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            total_profit=0
            tours = Order.objects.filter(agent=user)
            for i in tours:
                total_profit=total_profit+i.paid_by_user
            
            print(total_profit)
            context = {
                'Tours':tours,
                'Profit':total_profit
            }
            return render(request,'travelagency/booking_history.html',context=context)
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

def upcoming_tours(request,agentId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            tours = Order.objects.filter(agent=user)
            Tour=[]
            for i in tours:
                print(i)
                if i.tour.startDate > date.today():
                    Tour.append(i)
            context = {
                'Tours':Tour
            }
            return render(request,'travelagency/upcoming_tours.html',context=context)
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

def ongoing_tours(request,agentId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agentId == agentId:
            tours = Order.objects.filter(agent=user)
            Tour=[]
            for i in tours:
                if i.tour.startDate < date.today() and date.today() < i.tour.endDate :
                    Tour.append(i)
            context = {
                'Tours':Tour
            }
            return render(request,'travelagency/ongoing_tours.html',context=context)
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

def bookingNotification(request):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        order = Order.objects.filter(agent=user,status=True,agent_approval=False)
        context = {
            'Order':order,
        }
        return render(request,'travelagency/notification.html',context=context)
    else:
        return render(request,'forbidden.html')

def acceptOrder(request,orderId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if Order.objects.filter(order_id=orderId,agent=user).exists():
            order = Order.objects.get(order_id=orderId)
            order.agent_approval = True
            order.save()
            messages.success(request,"Congratualations! We atre glad that you get booking through us")
            return redirect('bookingNotification')
        else:
            return render(request,"forbidden.html")
    else:
        return render(request,'404.html')

def declineOrder(request,orderId):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if Order.objects.filter(order_id=orderId,agent=user).exists():
            order = Order.objects.get(order_id=orderId)
            cancelled_order = Cancelled_Order(
                order_id = order.order_id,
                tour = order.tour,
                customer = order.customer,
                customer_name = order.customer_name,
                customer_email = order.customer_email,
                customer_phone = order.customer_phone,
                customer_address = order.customer_address,
                agent = order.agent,
                agency = order.agency,
                total_people = order.total_people,
                paid_by_user = order.paid_by_user,
                total_price = order.total_price,
                creation_date = order.creation_date,
                cancelled_by = "AGENT",
            )
            cancelled_order.save()
            tour = order.tour
            tour.maximum_people+=order.total_people
            tour.save()
            order.delete()
            messages.error(request,'Our Executives will call you please provide us a valid reason for not accepting the offer')
            return redirect('/travelagency/booking-history/{}'.format(user.userAccess.agentId))
        else:
            return render(request,'forbidden.html')
    else:
        return render(request,'404.html')