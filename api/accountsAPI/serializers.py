from accounts.models import *
from rest_framework import serializers
from rest_framework import exceptions

class AgentRegisterSerializer(serializers.ModelSerializer):
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
        user.save()
        return user


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


