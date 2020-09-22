from django.urls import path
from .views import *

urlpatterns = [
    path('search',searchTour,name='searchTour'),
    path('tourdetails/<str:tourId>/<str:slug>',tourDetails,name='tourDetails'),
    path('booktour',bookTour,name='bookTour'),
    ]