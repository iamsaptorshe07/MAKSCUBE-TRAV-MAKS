from django.db import models
from accounts.models import *

    
class Tour(models.Model):
    TOUR_TYPE = (
        ('Family Special','Family Special'), 
        ('Friends Special','Friends Special'),
        ('Couple Friendly','Couple Friendly'),
        ('Solo Tour','Solo Tour'),
    )
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='agencyOwner')
    agency = models.ForeignKey(AgencyDetail,on_delete=models.CASCADE,related_name='tourAgency')
    tourId = models.CharField(max_length=30,unique=True)
    tourHeading = models.CharField(max_length=1000)
    tourSlug = models.SlugField(unique=True,max_length=255)
    startingLocation = models.CharField(max_length=300)
    endLocation = models.CharField(max_length=300)
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.TextField()
    inclusive = models.TextField()
    exclusive = models.TextField()
    highlight = models.TextField()
    price = models.FloatField()
    tour_type = models.CharField(max_length=500, choices=TOUR_TYPE)
    thumbnail = models.ImageField(upload_to="TourAccountThumbnail")
    othersThings = models.TextField(blank=True,null=True)
    tags = models.CharField(max_length=300,blank=True,null=True)
    nearestLocation1 = models.CharField(max_length=500, null=True,blank=True)
    nearestLocation1_distance = models.FloatField(null=True, blank=True)
    nlocationconnected1 = models.TextField(null=True, blank=True)
    nearestLocation2 = models.CharField(max_length=500, null=True,blank=True)
    nearestLocation2_distance = models.FloatField(null=True, blank=True)
    nlocationconnected2 = models.TextField(null=True, blank=True)
    nearestLocation3 = models.CharField(max_length=500, null=True,blank=True)
    nearestLocation3_distance = models.FloatField(null=True, blank=True)
    nlocationconnected3 = models.TextField(null=True, blank=True)
    nearestLocation4 = models.CharField(max_length=500, null=True,blank=True)
    nearestLocation4_distance = models.FloatField(null=True, blank=True)
    nlocationconnected4 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tourHeading


