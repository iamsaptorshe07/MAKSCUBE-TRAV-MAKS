from django.test import TestCase
from .models import *
import random,math,ast
from datetime import datetime
from datetime import date
# Create your tests here.
def OrderIdGenerator():
    
    charList='0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    uniqueId="x"
    for r in range(5):
        uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if Order.objects.filter(order_id=uniqueId).exists():
        uniqueId="k"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if Order.objects.filter(order_id=uniqueId).exists():
        uniqueId="p"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]
    
    if Order.objects.filter(order_id=uniqueId).exists():
        uniqueId="b"
        for r in range(5):
            uniqueId = uniqueId + charList[math.floor(random.random()*len(charList))]            
    return "".join(['TRAVMAKSORDER',uniqueId])

def canBook(lastDateOfBooking):
    print("\n\n\n",lastDateOfBooking,"\n\n\n")
    # d0=datetime.strptime(lastDateOfBooking, "%Y-%m-%d")
    # print("\n\n\n",d0,"\n\n\n")
    d1=date.today()
    if d1<lastDateOfBooking:
        return True
    else:
        return False 