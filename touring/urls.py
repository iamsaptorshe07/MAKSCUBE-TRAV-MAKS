from django.urls import path
from .views import *

urlpatterns = [
    #path('',travelagency_home,name='travelAgencyHome'),
    path('search',searchTour,name='searchTour'),
    ]