from django.urls import path
from .views import *

urlpatterns = [
        path('',TourAPIView.as_view(),name='Alltour'),
        path('compare-tour',compareTourView,name='CompareTourView'),
        path('<slug>',TourDetailsAPIView,name='TourDetail'),
    ]

