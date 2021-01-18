from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    #path('guide/account',sellerGuideSignup,name='guide_accounts_signup'),
    #path('guide/account/signup',guideSignup,name='guideSignup'),
    path('traveller/account/signup',travelerAccountsSignup,name='travelerAccountsSignup'),
    path('seller/account/signup', sellerAgencyAccountSignup, name='sellerAgencyAccountSignup'),
    path('seller/account/register-agency',agencyRegister,name='RegisterAgency'),
    
    #path('activate/guide/<uid>/<token>',activateGuide, name='activateGuide'),
    path('activate/seller/<uid>/<token>',activateSeller, name='activateSeller'),
    path('activate/traveller/<uid>/<token>',activateTraveller, name='activateTraveller'),
    
    #path('guide/login',guideLogin,name='Guide_Login'),
    path('traveller/login',travellerLogin,name='Traveller_Login'),
    path('seller/login',sellerLogin,name='Seller_login'),    

    path('user/logout',userLogout,name='userLogout'),

    path('editprofile/<str:account_type>/<int:uid>',userProfile,name='userProfile'),

    path('change-password',changePassword,name='ChnagePassword'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='accounts/changePassword.html'),name='password_reset'),
    path('password-reset/email-sent',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password-reset-form.html'),name='password_reset_confirm'),
    path('password-reset-done',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password-reset-complete.html'),name='password_reset_complete'),
    ] 