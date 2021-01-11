from django.urls import path
from .views import *

urlpatterns = [
        path('recent-added-tour',RecentAddedTour.as_view(),name='recentAddedTour'),
        path('solo-tour',SoloTour.as_view(),name='Solotour'),
        path('couple-tour',CoupleTour.as_view(),name='CoupleTour'),
        path('family-tour',FamilyTour.as_view(),name='FamilyTour'),
        path('friends-tour',FriendsTour.as_view(),name='FriendsTour'),
    ]

