from django.urls import path, include
from .views import *

urlpatterns = [
        #Travel Agency Signup
        path('travel-agent-signup',TravelAgentSignup.as_view(),name='travelAgentSignup'),

        #Travel Agency Login
        path('travel-agent-login',TravelAgentLogin.as_view(),name='TravelAgentLogin'),

        # Traveller Signup
        path('traveller-signup',TravellerSignup.as_view(),name='TravellerSignup'),

        # Traveller Login
        path('traveller-login',TravellerLogin.as_view(),name='TravellerLogin'),

        # User Profile
        path('user-profile',UserProfile.as_view(),name='UserProfile'),

        # Any user logout
        path('logout',LogoutView.as_view(),name='LogoutView'),

        # Agency Register
        path('agency-register',AgencyRegister.as_view(),name='AgencyRegister'),

        #Forgot Password / Reset Password
        path('password_reset/',include('django_rest_passwordreset.urls'), name='password_reset'),

        # Change Password
        path('change-password',ChangeMyPassword.as_view(),name='Chnagepassword')
]
    

