from django.urls import path
from .views import *

urlpatterns = [
    path('search',searchTour,name='searchTour'),
    path('all-tours',AllToursView.as_view(),name='allTours'),
    path('tourdetails/<str:tourId>/<str:slug>',tourDetails,name='tourDetails'),
    path('booktour/<tourId>/<agentId>',bookTour,name='bookTour'),
    path('paytm-payment-recieve',recievePayment,name='recievePayment')
    ]