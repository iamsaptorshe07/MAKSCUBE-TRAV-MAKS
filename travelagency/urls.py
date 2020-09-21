from django.urls import path
from .views import *

urlpatterns = [
    path('myagency/<agid>',travelagency_home,name='travelAgencyHome'),
    path('myagency/addtour/<int:uid>/<str:agid>',addTour,name='addTour'),
    path('agencytours/<int:uid>/<str:agid>',agencyTours,name='agencyTour'),
    path('agencytours/edit-tour',editTours,name='editTours'),
    ]