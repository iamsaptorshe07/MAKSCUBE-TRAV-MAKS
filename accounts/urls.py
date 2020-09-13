from django.urls import path
from .views import *
urlpatterns = [
    path('guide/account',sellerGuideSignup,name='guide_accounts_signup'),
    path('traveller/account',travelerAccounts,name='traveler_accounts_signup'),
    path('seller/account',sellerAgencyAccount,name='travelAgency_accounts_signup'),
    path('seller/account/register/agency/<int:id>',agencyRegister,name='RegisterAgency'),
    path('activate/seller/<uid>/<token>',activateSeller, name='activateSeller'),
    path('activate/traveller/<uid>/<token>',activateTraveller, name='activateTraveller'),
    path('traveller/login',travellerLogin,name='Traveller_Login'),
    path('seller/login',sellerLogin,name='Seller_login'),
    path('user/logout',userLogout,name='userLogout'),
    path('editprofile/<str:account_type>/<int:uid>',userProfile,name='userProfile'),
    path('change-password',changePassword,name='ChnagePassword')
    ] 