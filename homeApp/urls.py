from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('about-us',aboutUs,name='AboutUs'),
    path('contact-us',contactUs,name='ContactUs'),
    path('user-privacy-policy',userPrivacyPolicy,name='privacyPolicy'),
    path('user-FAQ',userFAQ,name='userFAQ'),
    path('user-payment-policy',userPaymentPolicy,name='userPaymentPolicy'),
    path('terms-and-condition',termsAndCondition,name='termsAndCondition'),
    path('partner/benifits-of-joing-travmaks',partnerBenifits,name='partnerBenifits'),
    path('benifits-of-joing-travmaks',partnerBenifitsTavellers,name='partnerBenifitsTavellers'),
    path('partnerportal-faq',partnerFAQ,name='partnerFAQ'),
    path('download-app',downloadApp,name='downloadApp'),
    path('beta',betaMode,name='betaMode'),
    ]