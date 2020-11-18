from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from accounts.models import *
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from accounts.tokens import activation_token
from django.conf import settings
# Create your views here.
def messages_sender(request,user):
    try:
        check_access_target = str(request.get_full_path()).split('/')
        print(check_access_target)
        if check_access_target[4]=='traveller-signup':
            email_temp = 'travellerMail'
        elif check_access_target[4]=='guide-signup':
            email_temp = 'guideMail'
        elif check_access_target[4]=='travelagent-signup':
            email_temp = 'sellerMail'
        else:
            return False
        site = get_current_site(request)
        mail_subject = 'Site Activation Link'
        message = render_to_string('{}.html'.format(email_temp), {
            'user': user,
            'domain': site,
            'uid':user.id,
            'token':activation_token.make_token(user)
                    })
        to_email=user.email
        to_list=[to_email]
        from_email=settings.EMAIL_HOST_USER
        print(from_email,'\n\n',message,'\n\n')
        send_mail(mail_subject,message,from_email,to_list,fail_silently=True)
        return True
    except Exception as e:
        print(e)
        return False

class TravelAgentSignup(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            account_field = ['email','name','DOB','phNo','gender','country','state','city','zipCode','address','password']
            goverment_proof = ['govIdType','govIdNo']
            if User.objects.filter(email=request.POST['email']).exists():
                email = request.POST.get('email')
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        data = {
                            'status':406,
                            'message':'User Already Exists'
                        }
                        return Response(data)
                    else:
                        my_data = request.POST
                        [account_data, gov_data] = map(lambda keys: {x: my_data[x] for x in keys}, [account_field, goverment_proof])
                        if GovId.objects.filter(user=user).exists():
                            print('exist')
                            data = {
                                'status':406,
                                'message':'Agency account verification mail has been send! Please verify your self!'
                            }
                            return Response(data)
                        else:
                            print("Come")
                            gov_data['user']=user
                            gov_data['govIdImage']=request.FILES.get('govIdImage')
                            gov_serializer = GovermentProofSerializer(data=gov_data)
                            if gov_serializer.is_valid():
                                user_data = gov_serializer.save()
                                res = messages_sender(request,user)
                                if res is True:
                                    data = {
                                        'status':200,
                                        'message':'Successfully Registered'
                                    }
                                       
                                else:
                                    data = {
                                        'status':500,
                                        'message':'SMTP Server Error'
                                    }
                                return Response(data)
                            else:
                                data = {
                                    'status':500,
                                    'message':gov_serializer.errors
                                }
                                return Response(data)
                else:
                    data = {
                        'status':'406',
                        'message':'Account already exsits! Check your email to activate the user account sent on {}'.format(user.creationTime)
                        }
                    return Response(data)
            else:
                my_data = request.POST
                img = request.FILES['govIdImage']
                print("\n",img,"\n")
                print("printed")
                [account_data, gov_data] = map(lambda keys: {x: my_data[x] for x in keys}, [account_field, goverment_proof])
                agent_serializer = AgentRegisterSerializer(data=account_data)
                print("Worked till here")
                gov_data['govIdImage']=img
                if agent_serializer.is_valid():
                    agent = agent_serializer.save()
                    gov_data['user']=agent.id
                    gov_serializer = GovermentProofSerializer(data=gov_data)
                    if gov_serializer.is_valid():
                        gov_serializer.save()
                        res = messages_sender(request,agent)
                        if res is True:
                            data = {
                                'status':200,
                                'message':"Please check your mail to activate your account"
                            }
                            return Response(data)
                        else:
                            data ={
                                'status':406,
                                'message':'SMTP Server occured'
                            }
                            return Response(data)
                    else:
                        data = {
                            'status':406,
                            'message':gov_serializer.errors
                        }
                        return Response(data)
                else:
                    data = {
                        'status':406,
                        'message':agent_serializer.errors
                    }
                    return Response(data)

                        





                     
