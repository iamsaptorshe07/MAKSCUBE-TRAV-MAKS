# Django Imports
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Account Info Import
from accounts.models import *
from accounts.tokens import activation_token
from django.contrib.auth.hashers import check_password
#Project Setting Import
from django.conf import settings

# Rest Framework Imports
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

#Login Imports 
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication



#----------------------------------- Code Logic ------------------------------------------------
#Activation Mail Sender
def messages_sender(request,user):
    try:
        print("message process started")
        check_access_target = str(request.get_full_path()).split('/')
        print(check_access_target)
        if check_access_target[4]=='traveller-signup':
            email_temp = 'travellerMail'
        elif check_access_target[4]=='guide-signup':
            email_temp = 'guideMail'
        elif check_access_target[4]=='travel-agent-signup':
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


# Travel - Agent Signup -----------------------------------------------
class TravelAgentSignup(APIView):
    def post(self, request, *args, **kwargs):
        account_field = ['email','name','DOB','phNo','gender','country','state','city','zipCode','address','password']
        goverment_proof = ['govIdType','govIdNo']
        if User.objects.filter(email=request.POST['email']).exists():
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            if user.is_active:
                if user.userAccess.agency_access is True:
                    data = {
                        'status':403,
                        'message':'User Already Exists'
                    }
                    return Response(data,status=status.HTTP_403_FORBIDDEN)
                else:
                    my_data = request.data
                    [account_data, gov_data] = map(lambda keys: {x: my_data[x] for x in keys}, [account_field, goverment_proof])
                    if GovId.objects.filter(user=user).exists():
                        data = {
                            'status':406,
                            'message':'Agency account verification mail has been send! Please verify your self!'
                        }
                        return Response(data)
                    else:
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
            my_data = request.data
            img = request.FILES['govIdImage']
            [account_data, gov_data] = map(lambda keys: {x: my_data[x] for x in keys}, [account_field, goverment_proof])
            agent_serializer = AccountSerializer(data=account_data)
            gov_data['govIdImage']=img
            if agent_serializer.is_valid():
                agent = agent_serializer.save()
                gov_data['user']=agent.id
                gov_serializer = GovermentProofSerializer(data=gov_data)
                if gov_serializer.is_valid():
                    gov_serializer.save()
                    res = messages_sender(request,agent)
                    print(res)
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


# ------------------- Travel Agent Sign Up Ends Here ------------------------

# Traveller Singup -----------------------------------------------------------
class TravellerSignup(APIView):
    def post(self,request):
        data = request.data
        print(data)
        email = data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                if user.userAccess.user_access is True:
                    return_data = {
                        'status':403,
                        'message':'User Already Exists'
                    }
                    return Response(data=return_data,status=status.HTTP_403_FORBIDDEN)
                else:
                    res = messages_sender(request,user)
                    if res is True:
                        return Response(
                            data = {
                                'status':200,
                                'message':'As your seller account already exists we will use your old account information, please verify your account to get the user access'
                            },
                            status = status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            data = {
                                'status':500,
                                'message':"Internal Problem Occured"
                            },
                            status = status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
            else:
                return Response(
                    data = {
                        'status':"",
                        'message':"Please Activate Your account first mail send on {}".format(user.creationTime)                    
                        },
                    status = status.HTTP_200_OK
                )
        else:
            userSerializer = AccountSerializer(data=request.data)
            if userSerializer.is_valid():
                user = userSerializer.save()
                print(user.id)
                res = messages_sender(request,user)
                if res is True:
                    return Response(
                        data = {
                            'status':200,
                            'message':'Account Created, Please Check the mail to verify your account'
                        },
                        status = status.HTTP_200_OK
                    )
                else:
                    return Response(
                        data = {
                            'status':500,
                            'message':'Internal Problem Occured'
                        },
                        status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    data = {
                        'staus':406,
                        'message':userSerializer.errors
                    },
                    status = status.HTTP_406_NOT_ACCEPTABLE
                )    




        
        

# Traveller Signup Ends here --------------------------------------------------

# Travel Agent Login --------------------------------------------------------
class TravelAgentLogin(APIView):
    def post(self,request):
        data = request.data
        email = data.get('email',"")
        password = data.get("password","")
        if email and password:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        user = authenticate(email=email, password=password)
                        if user is not None:
                            if AgencyDetail.objects.filter(user=user).exists():
                                agency = AgencyDetail.objects.get(user=user)
                                if agency.verified is True:
                                    login(request,user)
                                    request.session['access_type']='seller'
                                    token,created = Token.objects.get_or_create(user=user)
                                    return Response(
                                        {
                                            'token':token.key,
                                            'status':200,
                                            'message':'Successfully Loggedin'
                                        }
                                    )
                                else:
                                    return Response(
                                        {
                                            'status':404,
                                            'message':'Your Agency Is Under Review wait for one day, till we verify your account'
                                        }
                                    )
                            else:
                                login(request,user)
                                request.session['access_type']='seller'
                                token,created = Token.objects.get_or_create(user=user)
                                return Response(
                                    {   'token':token.key,
                                        'status':302,
                                        'message':'Redirect to Agency Register Page'
                                    }
                                )
                        else:
                            return Response(
                                {
                                    'status':404,
                                    'message':'Invalid Credentials'
                                }
                            )
                    else:
                        return Response(
                            {
                                'status':302,
                                'message':"Don't have any agent account redirect to travel agent signup page!"
                            }
                        )
                else:
                    return Response(
                        {
                            'status':404,
                            'message':'Check your mail sent on {} to activate the account'.format(user.creationTime)
                        }
                    )
            else:
                return Response(
                    {
                        'status':302,
                        'message':'No user does not exists!',
                    }
                )

        else:
            return Response(
                {
                    'status':404,
                    'message':'Email and Password Both Should Be Provided'
                }
            )
    
# Travel Agent Login Ends here --------------------------------------------------------

# Traveller - Noraml user Login --------------------------------------------------------
class TravellerLogin(APIView):
    def post(self,request):
        data = request.data
        email = data.get('email',"")
        password = data.get("password","")
        if email and password:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        user = authenticate(email=email, password=password)
                        if user is not None:
                            login(request,user)
                            request.session['access_type']='traveller'
                            token,created = Token.objects.get_or_create(user=user)
                            return Response(
                                {
                                    'token':token.key,
                                    'status':200,
                                    'message':'Successfully Loggedin'
                                }
                            )
                        
                        else:
                            return Response(
                                {
                                    'status':404,
                                    'message':'Invalid Credentials'
                                }
                            )
                    else:
                        return Response(
                            {
                                'status':302,
                                'message':"Don't have any user account redirect to user signup page!"
                            }
                        )
                else:
                    return Response(
                        {
                            'status':404,
                            'message':'Check your mail sent on {} to activate the account'.format(user.creationTime)
                        }
                    )
            else:
                return Response(
                    {
                        'status':302,
                        'message':'No user does not exists!',
                    }
                )

        else:
            return Response(
                {
                    'status':404,
                    'message':'Email and Password Both Should Be Provided'
                }
            )
        
# Traveller - Normal User Login Ends here -------------------------------------------------

# User Logout ------------------------------------------------------------------------------
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self,request):
        if request.session.session_key:
            print(request.session['access_type'])
            logout(request)
            return Response(
                {'status':204,
                'message':'Successfully Logout'}
            )
        else:
            return Response(
                {
                    'status':404,
                    'message':'No user to Logout!'
                }
            )

# ------------ User Logout Ends here --------------------------------------


# User Profile Visit, update Starts here  ------------------------------------------
class UserProfile(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    # To get the profile data
    def get(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                user_data = UserProfileSerializer(request.user)
                agency = AgencyDetail.objects.get(user = request.user)
                agency_data = AgencySerializer(agency)
                main_data = {
                    'status':200,
                    'user_data':user_data.data,
                    'agency_data':agency_data.data
                }
                return Response(main_data)
            elif request.session['access_type']=='traveller':
                user_data = UserProfileSerializer(request.user)
                return Response(
                    {
                        'status':200,
                        'user_data':user_data.data
                    }
                )
            else:
                return Response(
                    {
                        'status':404,
                        'message':'Wrong Access Type'
                    }
                )
        else:
            return Response(
                {
                    'status':404,
                    'message':"Not Authenticated"
                }
            )
    # To update the data
    def put(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller' or request.session['access_type']=='traveller':
                data = request.data
                user = request.user
                userserializer = AccountSerializer(user,data=data,partial=True)
                if userserializer.is_valid():
                    userserializer.save()
                    return Response(
                        {
                            'status':200,
                            'message':'Successfully Update'
                        }
                    )
                else:
                    return Response(userserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data ={
                'message':'Bad Request'
            }, status = status.HTTP_400_BAD_REQUEST,)

# User Profile Visit and update Ends here ----------------------------------

# Travel Agency Registration ----------------------------------
class AgencyRegister(APIView):
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    def post(self,request):
        if request.session.session_key:
            if request.session['access_type']=='seller':
                if AgencyDetail.objects.filter(user=request.user).exists() == False:
                    data = request.data.dict()
                    data['user']=request.user.id
                    data['agency_Id'] = 'AGEN'+str(request.user.userAccess.agentId[4:])
                    agency = AgencySerializer(data=data)
                    if agency.is_valid():
                        agency.save()
                        logout(request)
                        return Response(
                            {
                            'status':200,
                            'message':'Agency Registered, please wait till the time we verify your agency'
                            }
                        )
                    else:
                        return Response(
                            {
                            'status':404,
                            'message':'Some problem Occured'
                            }
                        )
                else:
                    return Response(
                        {
                            'status':404,
                            "message":"Already have a agency registered!"
                        }
                    )
            else:
                return Response(
                    {
                        'status':404,
                        'message':'Not Authorized to register your agency!'
                    }
                )
        else:
            return Response(
                {
                    'status':404,
                    'message':'Not Authenticated!'
                }
            )

# Travel Agency Registration Ends here ------------------------

# Change Password ---------------------------------------------
class ChangeMyPassword(APIView):
     authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
     def post(self,request):
         if request.session.session_key:
            data = request.data
            print(data)
            if check_password(data['oldpassword'],request.user.password):
                request.user.set_password(data['password'])
                request.user.save()
                return Response(
                    {
                        'status':200,
                        'message':'Password Changed Successfully!'
                    },
                    status = status.HTTP_200_OK
                    )
            else:
                return Response(
                    {
                        'status':406,
                        'message':'Enter correct current password'
                    },
                    status = status.HTTP_406_NOT_ACCEPTABLE
                )
        
         else:
             return Response(
                 {
                     'status':403,
                     'message':'Not Authenticated!'
                 },
                 status = status.HTTP_403_FORBIDDEN
             )
                
# Change Password ends here -----------------------------------