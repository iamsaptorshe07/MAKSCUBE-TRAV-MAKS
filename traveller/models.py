from django.db import models
from travelagency.models import *
from accounts.models import *
from touring.models import *
# Create your models here.

class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='wisher')
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE,name='wishedTour')
    creation_date = models.DateTimeField(auto_now_add=True)
    