from django.contrib import admin
from .models import *
from accounts.models import *
# Register your models here.
class TourDetailsAdmin(admin.ModelAdmin):
    model = Tour
    list_display = ('tourId','agency','get_seller_id','get_agency_id','publish_mode','creationDate','tourHeading',
    'startingLocation','endLocation','startDate','endDate',
    'price','tour_type','thumbnail','tags','maximum_people',
    )
    search_fields = ['tourId','tourHeading','agency__agency_Id']
    list_filter = ('tour_type',)

    def get_seller_id(self,obj):
        return obj.agency.user.userAccess.agentId
    get_seller_id.short_description = 'Seller ID'
    def get_agency_id(self, obj):
        return obj.agency.agency_Id
    get_agency_id.short_description = 'Agency ID'
'''    
class TourImageAdmin(admin.ModelAdmin):
    model=TourImage
    list_display = ('tour','image1','image2','image3','image4','image5','image6','image7',)
    search_fields = ['tour']
'''
admin.site.register(Tour,TourDetailsAdmin)#,TourImageAdmin)
