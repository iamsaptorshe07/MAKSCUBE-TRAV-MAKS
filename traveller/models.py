from django.db import models
from travelagency.models import Tour
from accounts.models import User
# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='wisher')
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name='wishedTour')
    creation_date = models.DateTimeField(auto_now_add=True)
    