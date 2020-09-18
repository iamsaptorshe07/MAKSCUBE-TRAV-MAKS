from django.urls import path
from .views import *

urlpatterns = [
    path('myagency/<uid>/<agid>',travelagency_home,name='travelAgencyHome')
    ]