from django.urls import path
from .views import *

urlpatterns = [
    path('preview/<str:tourId>',preview,name='preview'),
    path('advanced-search',advancedSearching,name='advancedSearching'),
    path('search',SearchTour.as_view(),name='searchTour'),
    path('all-tours',AllToursView.as_view(),name='allTours'),
    path('tourdetails/<str:tourId>/<str:slug>',tourDetails,name='tourDetails'),
    path('booktour/<tourId>/<agentId>',bookTour,name='bookTour'),
    path('paytm-payment-recieve',recievePayment,name='recievePayment'),
    path('tour-comparison',tourComparison,name='tourComparison'),
    ]