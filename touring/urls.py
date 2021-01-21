from django.urls import path
from .views import *

urlpatterns = [
    path('preview/<str:tourId>',preview,name='preview'),
    path('advanced-search',AdvancedSearching.as_view(),name='advancedSearching'),
    path('search',SearchTour.as_view(),name='searchTour'),
    path('all-tours',AllToursView.as_view(),name='allTours'),
    path('solo-tour',SoloTour.as_view(),name='SoloTour'),
    path('couple-tour',CoupleTour.as_view(),name='CoupleTour'),
    path('family-tour',FamilyTour.as_view(),name='FamilyTour'),
    path('friends-tour',FriendsTour.as_view(),name='FriendsTour'),
    path('tourdetails/<str:tourId>/<str:slug>',tourDetails,name='tourDetails'),
    path('booktour/<tourId>/<agentId>',bookTour,name='bookTour'),
    path('paytm-payment-recieve',recievePayment,name='recievePayment'),
    path('tour-comparison',tourComparison,name='tourComparison'),
    path('tour-query/<tourId>/<agentId>',tourQuery,name='tourQuery')
    ]