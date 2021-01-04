from .views import *
from django.urls import path

urlpatterns = [
    path('booking-history',bookingHistory,name='bookingHistory'),
    path('wishlist',wishList,name='wishlist'),
    path('write-review/<tourId>',writeReview,name='write-review'),
    path('generate-invoice/order=<orderID>',invoiceGenerator,name='invoiceGenerator'),
    path('ongoing-tours/<userId>',ongoingTour,name='ongoingTour'),
    path('upcoming-tours/<userId>',upcomingTour,name='upcomingTour'),
]