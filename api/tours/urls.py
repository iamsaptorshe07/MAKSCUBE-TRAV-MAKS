from django.urls import path
from .views import *

urlpatterns = [
        path('',TourAPIView.as_view(),name='Alltour'),
        path('search-tour',SearchTour.as_view(),name='SearchTour'),
        path('advanced-search-tour',AdvancedSearch.as_view(),name='AdvancedSearch'),
        path('compare-tour',compareTourView,name='CompareTourView'),
        path('<slug>',TourDetailsAPIView,name='TourDetail'),
    ]

