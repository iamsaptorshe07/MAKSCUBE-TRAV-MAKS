from rest_framework import serializers 
from touring.models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'order_id','tour','customer','customer_name','customer_email','customer_phone',
            'customer_address','agent','agency','total_people','paid_by_user','total_price'
        ]

        def create(self,validated_data):
            order = Order(
                order_id = validated_data['order_id'], 
                tour = validated_data['tour'], 
                customer = validated_data['customer'],
                customer_name = validated_data['customer_name'],
                customer_email = validated_data['customer_email'],
                customer_address = validated_data['customer_address'],
                agent = validated_data['agent'],
                agency = validated_data['agency'],
                total_people = validated_data['total_people'],
                paid_by_user = validated_data['paid_by_user'],
                total_price = validated_data['total_price']
            )
            order.save()
            return order