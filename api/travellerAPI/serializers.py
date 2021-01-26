from rest_framework import serializers 
from traveller.models import WishList

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = [
            'user','tour','creation_date'
        ]

