from django.test import TestCase
from accounts.models import *
from .models import *
import random,math,ast
from datetime import date
# Create your tests here.



def tourIdMaker():
    
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="x"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if Tour.objects.filter(tourId=uniqueId).exists():
        uniqueId="k"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if Tour.objects.filter(tourId=uniqueId).exists():
        uniqueId="p"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if Tour.objects.filter(tourId=uniqueId).exists():
        uniqueId="b"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TRAVMAKSTOUR',uniqueId])

#2000-12-26
def tourDate(sdate):
    print("\n\n",sdate,"\n\n")
    if sdate[4] != '-':
        d,m,y=sdate.split('/')
        fDate = y+'-'+m+'-'+d
        return fDate
    else:
        return sdate


def tourDuration1(sdate,edate):
    d1=date(tourDate(sdate))
    d0=date(tourDate(edate))

    duration = d1-d0
    return duration.days


def tourDuration(sdate,edate):
    print("\n\n",sdate,edate,"\n\n")
    if  edate[4] == '-':
        y,m,d=edate.split('-')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nIf Edate : ",y,m,d)
        d1=date(y,m,d)
    else:
        d,m,y=edate.split('/')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nEdate : ",y,m,d)
        d1=date(y,m,d)
    if  sdate[4] == '-':
        y,m,d=sdate.split('-')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nIf Sdate : ",y,m,d)
        d0=date(y,m,d)
    else:
        d,m,y=sdate.split('/')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nSdate : ",y,m,d)
        d0=date(y,m,d)
    
    duration = d1-d0
    return duration.days


# def descriptionMaker(description_dct):
#     description = 'TRAVMAKS'
#     description = description + str(description_dct)
#     description = description.replace(' ','--')
#     return description+'TRAVMAKS'

# def descriptionExtractor(description_str):
#     description_str = description_str.strip('TRAVMAKS')
#     description = ast.literal_eval(description_str)
#     return description

# def testDec(dictionarywww):
#     print("Actual dic : \n",type(dictionarywww),"\n",dictionarywww)
#     x=descriptionMaker(dictionarywww)
#     print("\n\nDic to String :\n",type(x),"\n",x)
#     y=descriptionExtractor(x)
#     print("\n\nString to Dic :\n",type(y),"\n",y)

#automatically add tour
def makeTour():
    tours = Tour.objects.get()
    
    for tour in tours:
        user = tour.seller
        sdate = tour.startDate
        edate =tour.endDate

        special_tour_type=tour.special_tour_type
        specialOffer = tour.specialOffer
        if specialOffer:
            specialOfferDescription = str(tour.specialOfferDescription).strip()

        slocation = tour.startDate
        elocation = tour.endDate
        price = tour.price
        maximum_people = tour.maximum_people
        ttype = tour.tour_type
        thumbnail = tour.thumbnail
        ttitle = tour.tourHeading
        inclusive = tour.inclusive
        exclusive = tour.exclusive
        highlight = tour.highlight
        overview = tour.overview
        tourId = tourIdMaker()
        print('\n\n',tourId,'\n\n')
        slug = ''
        for character in ttitle:
            if character.isalnum():
                slug+=character
        slug+='_tourfrom_{}to{}_startingfrom{}_by{}-{}_tourId-{}_{}'.format(
            slocation,elocation,sdate,agid,uid,tourId,ttype
        )
        print('\n\n',slug,'\n\n')
        description = tour.description
        last_booking_date = tour.last_booking_date
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

#automatically add tour

''' Testing URL Handlere '''
from django.shortcuts import render,redirect
def testURL(request):
    return render(request,'travelagency/travelagency_basetemplate.html')
