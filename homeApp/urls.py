from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('about-us',aboutUs,name='AboutUs'),
    path('contact-us',contactUs,name='ContactUs')
    ]