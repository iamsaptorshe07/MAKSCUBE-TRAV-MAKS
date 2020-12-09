from accounts.models import *
from rest_framework import serializers
from rest_framework import exceptions

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email','name','DOB','phNo','gender','country','state','city','zipCode','address','password'
        ]

    def create(self,validate_data):
        print(validate_data)
        user = User(
            email = validate_data['email'],
            name = validate_data['name'],
            DOB = validate_data['DOB'],
            phNo = validate_data['phNo'],
            gender = validate_data['gender'],
            country = validate_data['country'],
            state = validate_data['state'],
            city = validate_data['city'],
            zipCode = validate_data['zipCode'],
            address = validate_data['address']
        )
        password = validate_data['password']
        user.set_password(password)
        user.is_active = False
        user.save()
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email','name','DOB','phNo','gender','country','state','city','zipCode','address'
        ]

class AgentAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['user','agency_access','agentId']

        def create(self,validate_data):
            account_type = AccountType(
                user = validate_data['user'],
                agency_access = validate_data['agency_access'],
                agentId = validate_data['agentId']
            )
            account_type.save()
            return account_type

class GovermentProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovId
        fields = '__all__'

        def create(self,validate_data):
            gov_proof = GovId(
                user = validate_data['user'],
                govIdType = validate_data['govIdType'],
                govIdNo = validate_data['govIdNo'],
                govIdImage = validate_data['govIdImage']
            )
            gov_proof.save()
            return gov_proof


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyDetail
        fields = [
            'user',
            'agencyName','agency_Id','agencyPhNo','agencyCountry','agencyCity','agencyState',
            'agencyZipCode','govApproved','govApprovedId','agencyAddress'
        ]
        def create(self,validate_data):
            agency = AgencyDetail(
                user = validate_data['user'],
                agencyName = validate_data['agencyName'],
                agency_Id = validate_data['agency_Id'],
                agencyPhNo = validate_data['agencyPhNo'],
                agencyCountry = validate_data['agencyCountry'],
                agencyCity = validate_data['agencyCity'],
                agencyState = validate_data['agencyState'],
                agencyZipCode = validate_data['agencyZipCode'],
                govApproved= validate_data['govApproved'],
                govApprovedId = validate_data['govApprovedId'],
                agencyAddress = validate_data['agencyAddress']

            )
            agency.save()
            return agency