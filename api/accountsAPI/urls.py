from django.urls import path
from .views import *

urlpatterns = [
        path('travelagent-signup',TravelAgentSignup.as_view(),name='travelAgentSignup'),
    ]