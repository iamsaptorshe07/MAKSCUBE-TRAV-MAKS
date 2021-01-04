from django.db import models
from accounts.models import *
from PIL import Image
    
class Tour(models.Model):
    TOUR_TYPE = (
        ('Family-Special','Family-Special'), 
        ('Friends-Special','Friends-Special'),
        ('Couple-Friendly','Couple-Friendly'),
        ('Solo-Tour','Solo-Tour'),
        ('All','All')
    )
    SPECIAL_TOUR_TYPE = (
        ('Bike-tours','Bike-tours'),
        ('Self-drive','Self-drive'),
        ('Trecking-Special','Trecking-Special'),
        ('None','None')
    )
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='agencyOwner')
    agency = models.ForeignKey(AgencyDetail,on_delete=models.CASCADE,related_name='tourAgency')
    maximum_people = models.IntegerField(default=30)
    tourId = models.CharField(max_length=30,unique=True)
    tourHeading = models.CharField(max_length=1000)
    tourSlug = models.CharField(unique=True,max_length=255)
    startingLocation = models.CharField(max_length=300)
    endLocation = models.CharField(max_length=300)
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.TextField()
    overview = models.TextField(null=True,blank=True)
    inclusive = models.TextField()
    exclusive = models.TextField()
    highlight = models.TextField()
    price = models.FloatField()
    tour_type = models.CharField(max_length=50, choices=TOUR_TYPE)
    special_tour_type=models.CharField(max_length=50, choices=SPECIAL_TOUR_TYPE,default='None')
    thumbnail = models.ImageField(upload_to="TourAccountThumbnail")
    last_booking_date = models.DateField()
    specialOffer = models.BooleanField(default=False)
    specialOfferDescription = models.TextField(blank=True,null=True)

    creationDate = models.DateField(auto_now_add=True)
    othersThings = models.TextField(blank=True,null=True)
    tags = models.CharField(max_length=300,blank=True,null=True)
    
    publish_mode = models.BooleanField(default=False)

    #### resize image
    def save(self):
        super().save()
        img = Image.open(self.thumbnail.path)
        output_size = (468 , 312)
        img.resize(output_size)
        if img.height > 468 or img.width >312 :
            output_size = (468 , 312)
            img.resize(output_size)
            #img.thumbnail(output_size)
            img.save(self.thumbnail.path)
        
    def __str__(self):
        return self.tourHeading


class TourImage(models.Model):
    tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to="TourPreview")
    image2 = models.ImageField(upload_to="TourPreview",null=True,blank=True)
    image3 = models.ImageField(upload_to="TourPreview",null=True,blank=True)
    image4 = models.ImageField(upload_to="TourPreview",null=True,blank=True)
    image5 = models.ImageField(upload_to="TourPreview",null=True,blank=True)
    image6 = models.ImageField(upload_to="TourPreview",null=True,blank=True)
    image7 = models.ImageField(upload_to="TourPreview",null=True,blank=True)

class TourQuery(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name='tourQuery')
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name='agent')
    subject = models.CharField(max_length=500)
    query = models.TextField()


class Review(models.Model):
    rating = models.IntegerField(null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name='tour')


