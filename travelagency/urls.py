from django.urls import path
from .views import *

urlpatterns = [
    path('myagency/<agid>',travelagency_home,name='travelAgencyHome'),
    path('myagency/addtour/<int:uid>/<str:agid>',addTour,name='addTour'),
    path('agencytours/<int:uid>/<str:agid>',agencyTours,name='agencyTour'),
    path('agencytours/edit-tour/<str:agentId>/<str:tourId>',editTours,name='editTours'),
    path('agencytours/delete-tour/<agentId>/<tourId>',deleteteTour,name='deleteteTour'),
    path('booking-history/<agentId>',booking_history,name='bookingHistory'),
    path('upcoming-tours/<agentId>',upcoming_tours,name='upcomingTours'),
    path('ongoing-tours/<agentId>',ongoing_tours,name='ongoingTours')
]