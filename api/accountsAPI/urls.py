from django.urls import path
from .views import *

urlpatterns = [
        #Travel Agency Signup
        path('travel-agent-signup',TravelAgentSignup.as_view(),name='travelAgentSignup'),
        #Travel Agency Login
        path('travel-agent-login',TravelAgentLogin.as_view(),name='TravelAgentLogin'),
        # Traveller Login
        path('traveller-login',TravellerLogin.as_view(),name='TravellerLogin'),
        # Any user logout
        path('logout',LogoutView.as_view(),name='LogoutView')
    ]

