from django.urls import path
from .views import *

urlpatterns = [
        path('my-agency-tours',MyAgencyTour.as_view(),name='MyAgencyTour'),
        path('my-agency-tour-detail/<tourId>',TourDetail.as_view(),name='TourGetEditDelete'),
        path('ongoing-tour',OngoingTour.as_view(),name='OngoingTour'),
        path('accept-decline-tour/<orderId>',AcceptOrDeclineTour.as_view(),name='AcceptOrDecline'),
    ]
