from django.contrib import admin
from .models import *
from accounts.models import *
# Register your models here.
class TourDetailsAdmin(admin.ModelAdmin):
    model = Tour
    list_display = ('tourId','agency','get_seller_id','get_agency_id','tourHeading','startingLocation','endLocation','startDate','endDate',
    'highlight','price','tour_type','thumbnail','tags',
    'nearestLocation1','nearestLocation1_distance', 'nlocationconnected1',
    'nearestLocation2','nearestLocation2_distance', 'nlocationconnected2',
    'nearestLocation3','nearestLocation3_distance', 'nlocationconnected3',
    'nearestLocation4','nearestLocation4_distance', 'nlocationconnected4',
    )
    search_fields = ['tourId','tourHeading','agency__agency_Id']
    list_filter = ('tour_type',)

    def get_seller_id(self,obj):
        return obj.agency.user.userAccess.agentId
    get_seller_id.short_description = 'Seller ID'
    def get_agency_id(self, obj):
        return obj.agency.agency_Id
    get_agency_id.short_description = 'Agency ID'
    


admin.site.register(Tour,TourDetailsAdmin)
