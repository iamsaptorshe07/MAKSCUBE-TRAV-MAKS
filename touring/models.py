from django.db import models
from accounts.models import *
from travelagency.models import *
from datetime import datetime
# Create your models here.
class Order(models.Model):
    order_id = models.CharField(max_length=255,unique=True)
    tour = models.ForeignKey(Tour,on_delete = models.CASCADE,related_name='Tour')
    customer = models.ForeignKey(User,on_delete = models.CASCADE,related_name='customer')
    customer_name = models.CharField(max_length=500)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.CharField(max_length=600)
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name='Agent')
    agency = models.ForeignKey(AgencyDetail,on_delete=models.CASCADE,related_name='Agency')
    total_people = models.IntegerField()
    paid_by_user = models.FloatField()
    total_price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True,)
    status = models.BooleanField(default=False)
    agent_approval = models.BooleanField(default=False)
    user_cancel =models.BooleanField(default=False)

    def __str__(self):
        return self.order_id

class Payment(models.Model):
    Order = models.OneToOneField(Order,on_delete=models.CASCADE, related_name='Order')
    transaction_id = models.CharField(max_length=255,unique=True,default='test')
    banktransaction_id = models.CharField(max_length=255,unique=True,default='test')
    txn_date = models.DateTimeField(auto_now_add=True,null=True)
    gateway_name = models.CharField(max_length=100,default='test')
    bankname = models.CharField(max_length=200,default='test')
    payment_mode = models.CharField(max_length=200,default='test')
    creation_date = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.transaction_id

class Failed_Order(models.Model):
    order_id = models.CharField(max_length=255,unique=True)
    tour = models.ForeignKey(Tour,on_delete = models.CASCADE,related_name='FTour')
    customer = models.ForeignKey(User,on_delete = models.CASCADE,related_name='Fcustomer')
    customer_name = models.CharField(max_length=500)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.CharField(max_length=600)
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name='FAgent')
    agency = models.ForeignKey(AgencyDetail,on_delete=models.CASCADE,related_name='FAgency')
    total_people = models.IntegerField()
    paid_by_user = models.FloatField()
    total_price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.order_id


class Cancelled_Order(models.Model):
    CANCELLED_BY = (
        ('AGENT','AGENT'),
        ('USER','USER'),
    )
    order_id = models.CharField(max_length=255,unique=True)
    tour = models.ForeignKey(Tour,on_delete = models.CASCADE,related_name='CTour')
    customer = models.ForeignKey(User,on_delete = models.CASCADE,related_name='Ccustomer')
    customer_name = models.CharField(max_length=500)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.CharField(max_length=600)
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name='CAgent')
    agency = models.ForeignKey(AgencyDetail,on_delete=models.CASCADE,related_name='CAgency')
    total_people = models.IntegerField()
    paid_by_user = models.FloatField()
    total_price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True,null=True)
    cancelled_by = models.CharField(max_length=200,choices=CANCELLED_BY)
    cancel_reason = models.TextField(null=True,blank=True)



