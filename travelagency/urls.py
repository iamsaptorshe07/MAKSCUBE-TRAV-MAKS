from django.urls import path
from .views import *

urlpatterns = [
    path('travelagency',travelagency_home,name='travelAgencyHome')
    ]