from .views import *
from django.urls import path

urlpatterns = [
    path('booking-history',bookingHistory,name='bookingHistory'),
    path('wishlist',wishList,name='wishlist'),
    path('generate-invoice/order=<orderID>',invoiceGenerator,name='invoiceGenerator'),
    path('ongoing-tours/<userId>',ongoingTour,name='ongoingTour'),
    path('upcoming-tours/<userId>',upcomingTour,name='upcomingTour'),
]