from django.urls import path
from .views import *

urlpatterns = [
        #Travel Agency Signup
        path('travel-agent-signup',TravelAgentSignup.as_view(),name='travelAgentSignup'),
        #Travel Agency Login
        path('travel-agent-login',TravelAgentLogin.as_view(),name='TravelAgentLogin'),
        # Traveller Login
        path('traveller-login',TravellerLogin.as_view(),name='TravellerLogin'),
        # User Profile
        path('user-profile',UserProfile.as_view(),name='UserProfile'),
        # Any user logout
        path('logout',LogoutView.as_view(),name='LogoutView'),
        # Agency Register
        path('agency-register',AgencyRegister.as_view(),name='AgencyRegister')
    ]

