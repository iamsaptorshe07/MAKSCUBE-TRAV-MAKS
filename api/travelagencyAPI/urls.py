from django.urls import path
from .views import *

urlpatterns = [
        path('my-agency-tours',MyAgencyTour.as_view(),name='MyAgencyTour'),
        path('my-agency-tour-detail/<tourId>',TourDetail.as_view(),name='TourGetEditDelete'),
        path('ongoing-tour',OngoingTour.as_view(),name='OngoingTour'),
        path('upcoming-tour',UpcomingTour.as_view(),name='UpcomingTour'),
        path('order-booking-history',OrderBookingHistory.as_view(),name='OrderBookingHistory'),
        path('my-incoming-order-stack',IncomingOrderStack.as_view(),name='IncomingOrderStack'),
        path('accept-decline-tour/<orderId>',AcceptOrDeclineTour.as_view(),name='AcceptOrDecline'),
    ]
