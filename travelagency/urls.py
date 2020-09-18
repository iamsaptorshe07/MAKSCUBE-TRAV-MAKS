from django.urls import path
from .views import *

urlpatterns = [
    path('myagency/<agid>',travelagency_home,name='travelAgencyHome'),
    path('myagency/addtour/<uid>/<agid>',addTour,name='addTour'),
    ]