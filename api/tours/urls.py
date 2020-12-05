from django.urls import path
from .views import *

urlpatterns = [
        path('',TourAPIView.as_view(),name='Alltour'),
        path('<slug>',TourDetailsAPIView,name='TourDetail'),
    ]

