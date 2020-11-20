from .views import *
from django.urls import path

urlpatterns = [
    path('booking-history/<userId>/',bookingHistory,name='bookingHistory'),
    path('generate-invoice/order=<orderID>',invoiceGenerator,name='invoiceGenerator'),
    path('ongoing-tours',ongoingTour,name='ongoingTour'),
    path('upcoming-tours',upcomingTour,name='upcomingTour'),
]