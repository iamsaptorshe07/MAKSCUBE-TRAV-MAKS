from django.urls import path
from .views import *

urlpatterns = [
        path('my-agency-tours',MyAgencyTour.as_view(),name='MyAgencyTour'),
    ]
