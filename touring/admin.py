from django.contrib import admin
from .models import *
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id','get_tour','tour_id','get_customer_email','customer_name','customer_email',
        'customer_phone','customer_address','get_agent_email','agency_name','agency_id','total_people',
        'per_people_price','total_price','paid_by_user','creation_date','status','agent_approval','user_cancel'
    ]
    def get_customer_email(self,obj):
        return obj.customer.email
    def get_agent_email(self,obj):
        return obj.agent.email
    def agency_name(self,obj):
        return obj.agency.agencyName
    def get_tour(self,obj):
        return obj.tour.tourHeading
    def tour_id(self,obj):
        return obj.tour.tourId
    def agency_id(self,obj):
        return obj.agency.agency_Id
    def per_people_price(self,obj):
        return obj.tour.price

    get_customer_email.short_description = 'Booking Account Email'
    get_agent_email.short_description = 'Agent Email'
    get_tour.short_description = 'Tour'

    search_fields = ['order_id','customer__email','customer_email','agency__agency_Id']
    list_filter = ('status',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id','order_id','banktransaction_id','txn_date',
        'gateway_name','bankname','payment_mode','creation_date'
    ]
    def order_id(self,obj):
        return obj.Order.order_id

    search_fields = ['Order__order_id','transaction_id','banktransaction_id']
    list_filter = ('bankname','gateway_name','payment_mode')
    

admin.site.register(Order,OrderAdmin)
admin.site.register(Failed_Order)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Cancelled_Order)
admin.site.register(TourQuery)