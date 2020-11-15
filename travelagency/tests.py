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
    if sdate[4] != '-':
        m,d,y=sdate.split('/')
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
    if  edate[4] != '-':
        m,d,y=edate.split('/')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nIf Edate : ",y,m,d)
        d1=date(y,m,d)
    else:
        y,m,d=edate.split('-')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nEdate : ",y,m,d)
        d1=date(y,m,d)
    if  sdate[4] != '-':
        m,d,y=sdate.split('/')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nIf Sdate : ",y,m,d)
        d0=date(y,m,d)
    else:
        y,m,d=sdate.split('-')
        y=int(y)
        m=int(m)
        d=int(d)
        print("\n\nSdate : ",y,m,d)
        d0=date(y,m,d)
    
    duration = d1-d0
    return duration.days


def descriptionMaker(description_dct):
    description = 'TRAVMAKS'
    description = description + str(description_dct)
    description = description.replace(' ','--')
    return description+'TRAVMAKS'

def descriptionExtractor(description_str):
    description_str = description_str.strip('TRAVMAKS')
    description = ast.literal_eval(description_str)
    return description

def testDec(dictionarywww):
    print("Actual dic : \n",type(dictionarywww),"\n",dictionarywww)
    x=descriptionMaker(dictionarywww)
    print("\n\nDic to String :\n",type(x),"\n",x)
    y=descriptionExtractor(x)
    print("\n\nString to Dic :\n",type(y),"\n",y)



''' Testing URL Handlere '''
from django.shortcuts import render,redirect
def testURL(request):
    return render(request,'travelagency/travelagency_basetemplate.html')
