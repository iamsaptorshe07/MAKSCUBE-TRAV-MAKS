# Import necesary libraries --------------------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.http import *
from .models import *
from .uniqueKey import *
from django.contrib import messages
from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .tokens import activation_token 
from django.utils.dateparse import parse_date
from django.conf import settings
from django.contrib.auth.hashers import check_password
#from django.template import RequestContext
# Importing ends here ---------------------

def messages_sender(request,user):
    try:
        check_access_target = str(request.get_full_path()).split('/')
        print(check_access_target)
        if check_access_target[2]=='traveller':
            email_temp = 'travellerMail'
        elif check_access_target[2]=='guide':
            email_temp = 'guideMail'
        elif check_access_target[2]=='seller':
            email_temp = 'sellerMail'
        else:
            return False
        site = get_current_site(request)
        mail_subject = 'Travmaks Account Activation Link'
        context={
            'user': user.name,
            'domain': site,
            'uid':user.id,
            'token':activation_token.make_token(user)                   
        }
        html_message = render_to_string('{}.html'.format(email_temp),context=context)
        message = strip_tags(html_message)
        to_email_list=[user.email]
        from_email=settings.EMAIL_HOST_USER
        print(from_email,'\n\n',message,'\n\n',to_email_list,'\n\n')
        email = EmailMultiAlternatives(
            mail_subject,
            message,
            from_email,
            to_email_list
        )
        email.attach_alternative(html_message,"text/html")
        email.send()
        return True
    except Exception as e:
        print(e)
        return False

def activateTraveller(request, uid, token):
    if len(User.objects.filter(id=uid))>0:
        user = User.objects.get(id=uid)
        if user is not None and activation_token.check_token(user,token):
            if user.is_active:
                if user.userAccess.user_access:
                    return render(request,'404.html')
                else:
                    userAccess = AccountType.objects.get(user=user)
                    userAccess.user_access = True
                    userAccess.userId=travellerId()
                    user.save()
                    userAccess.save()
            else:
                user.is_active= True
                access = AccountType(user=user,user_access=True,userId=travellerId())
                user.save()
                access.save()
            messages.success(request,'Account activated please login')
            return redirect('Traveller_Login')
        else:
            return render(request,'404.html')
    else:
        return render(request,'404.html')
'''
This function is responsible for sending the account(Seller - Agency and guide) creation and login page to the front - end and also 
responsible for handling the signup request of the sellers (Travel agency not guide)
'''
def activateSeller(request, uid, token):
    if User.objects.filter(id=uid).exists():
        user = User.objects.get(id=uid)
        if user is not None and activation_token.check_token(user,token):
            if user.is_active:
                if user.userAccess.agency_access:
                    return render(request,'404.html')
                else:
                    userAccess = AccountType.objects.get(user=user)
                    userAccess.agency_access = True
                    userAccess.agentId=sellerId()
                    user.save()
                    userAccess.save()
            else:
                user.is_active = True
                access =AccountType(user=user,agency_access=True,agentId=sellerId())
                user.save()
                access.save()
            messages.success(request,'Account Activated, Please Login to register your agency')
            return redirect('Seller_login')
        else:
            return render(request,'404.html')
    else:
        return render(request,'404.html')


# Traveller account creation and login page handler and also signup of traveller handler function ---- Old one

# Traveller Signup Main Page
def travelerAccountsSignup(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            phNo = request.POST.get('phone')
            print(email, phNo)
            if User.objects.filter(phNo=phNo, email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        messages.warning(request, 'Your account is already exsits! Please login!')
                        return redirect('travelerAccountsSignup')
                    else:
                        res = messages_sender(request, user)
                        print(res)
                        if res is True:
                            messages.success(request,'As your seller account already exists we will use your old data just Check your email to activate the user account')
                            return redirect('travelerAccountsSignup')
                        if res is False:
                            messages.error(request, 'Internal Problem Occured')
                            return redirect('travelerAccountsSignup')
                else:
                    messages.warning(request, 'Account already exsits! Please verify your email! sent on {}'.format(
                        user.creationTime))
                    return redirect('travelerAccountsSignup')
            elif User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        messages.warning(request, 'Your account is already exsits! Please login!')
                        return redirect('travelerAccountsSignup')
                    else:
                        res = messages_sender(request, user)
                        print(res)
                        if res is True:
                            messages.success(request,
                                             'As your seller account already exists we will use your old data just Check your email to activate the user account')
                            return redirect('travelerAccountsSignup')
                        if res is False:
                            messages.error(request, 'Internal Problem Occured')
                            return redirect('travelerAccountsSignup')
                        return redirect('sellerAgencyAccountSignup')
                else:
                    messages.warning(request, 'Account already exsits! Please verify your email! sent on {}'.format(
                        user.creationTime))
                    return redirect('travelerAccountsSignup')
            elif User.objects.filter(phNo=phNo).exists():
                user = User.objects.get(phNo=phNo)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        messages.warning(request, 'Your account is already exsits! Please login!')
                        return redirect('travelerAccountsSignup')
                    else:
                        messages.warning(request,'Agency account already exsits! Check your email to activate the user account!')

                        return redirect('sellerAgencyAccountSignup')
                else:
                    messages.warning(request, 'Account already exsits! Please verify your email!')
                    return redirect('travelerAccountsSignup')
            elif len(str(request.POST.get('address')))>100:
                messages.warning(request, 'Address is too big!')
                return redirect('travelerAccountsSignup')
            else:
                user = User(
                    name=request.POST.get('name'),
                    email=email,
                    gender=request.POST.get('gender'),
                    DOB=request.POST.get('bdate'),
                    phNo=request.POST.get('phone'),
                    country=request.POST.get('country'),
                    state=request.POST.get('state'),
                    city=request.POST.get('city'),
                    address=request.POST.get('address'),
                    zipCode=request.POST.get('zip')
                )
                user.set_password(request.POST.get('password1'))
                user.is_active = False
                user.save()
                res = messages_sender(request, user)
                print("Email return :",res)
                if res is True:
                    messages.success(request, ' email to activatCheck youre the account')
                    return redirect('travelerAccountsSignup')
                if res is False:
                    user.delete()
                    messages.error(request, 'Internal Problem Occured')
                    return redirect('travelerAccountsSignup')
        except Exception as e:
            print(e)
            return redirect('/')
    else:
        return render(request, 'accounts/traveller_signup.html')

# Traveller Signup Ends here
#--------------------------------------------------------------------------------------------------
# Traveller log in starts here
def travellerLogin(request):
    if request.method=='POST':
        try:        
            email=request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        user = auth.authenticate(email=email, password=password)
                        if user is not None:
                            auth.login(request,user)
                            request.session['access_type']='traveller'
                            messages.success(request,'Successfully Loggedin')
                            return redirect('/')
                        else:
                            messages.error(request,'Invalid Credential')
                            return redirect('Traveller_Login')
                    else:
                        messages.warning(request,"You don't have any user account, Please register yourself as an user")
                        return redirect('travelerAccountsSignup')
                else:
                    messages.warning(request,'Check your mail sent on {}'.format(user.creationTime))
                    return redirect('/')
            else:
                messages.error(request,"Please Signup before Login")
                return redirect('travelerAccountsSignup')
        except Exception as problem:
            messages.warning(request, problem)
            return redirect('Traveller_Login')
    else:
        return render(request,'accounts/traveller_login.html')
# Traveller Login handler Ends here-------------------------------------------------------------
# Agency Login handler Starts here ----------------------------------------
def sellerLogin(request):
    if request.method=='POST':
        try:        
            email=request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        user = auth.authenticate(email=email, password=password)
                        if user is not None:
                            if AgencyDetail.objects.filter(user=user).exists():
                                agency = AgencyDetail.objects.get(user=user)
                                if agency.verified is True:
                                    auth.login(request,user)
                                    request.session['access_type']='seller'
                                    messages.success(request,'Successfully Loggedin')
                                    return redirect('/')
                                else:
                                    messages.warning(request,"Please wait for one day till we verified your account")
                                    return redirect('Seller_login')
                            else:
                                auth.login(request,user)
                                request.session['access_type']='seller'
                                messages.warning(request,'Register Your Agency inorder to proceed')
                                return redirect('RegisterAgency')
                        else:
                            messages.error(request,'Invalid Credential')
                            return redirect('Seller_login')
                    else:
                        messages.warning(request,"You don't have any agency account, Please register yourself as an user")
                        return redirect('sellerAgencyAccountSignup')
                else:
                    messages.warning(request,'Check your mail sent on {} to activate the account'.format(user.creationTime))
                    return redirect('/')
            else:
                messages.error(request,"Please Signup before Login")
                return redirect('sellerAgencyAccountSignup')
        except Exception as problem:
            messages.warning(request, problem)
            return redirect('Seller_login')
    else:
        return render(request,'accounts/seller_login.html')
# Agency Login handler Ends here-------------------------------------------------------------

# Any User Logout strts here --------------
def userLogout(request):
    try:
        auth.logout(request)
        messages.success(request,'Successfully Logged Out')
        return redirect('/')
    except Exception as problem:
        print(problem)
        messages.success(request,'Sorry, Internal Problem Occured')
        return redirect('/')
# User logout ends here --------------

# Seller (Agency and Guide) account creation and login page handler and also signup of seller handler function ----
def sellerAgencyAccountSignup(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            phNo = request.POST.get('phone') 
            if User.objects.filter(phNo=phNo,email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        messages.warning(request,'Your agency account is already exsits! Please login!')
                        return redirect('sellerAgencyAccountSignup')
                    else:
                        if GovId.objects.filter(user=user).exists():
                            messages.warning(request,'Agency account verification mail has been send! Please verify your self!')
                            return redirect('sellerAgencyAccountSignup')
                        else:
                            
                            govData = GovId(
                            user=user,
                            govIdType=request.POST.get('govIdName'),
                            govIdNo = request.POST.get('govIdNo'),
                            govIdImage = request.FILES.get('govIdImage')
                            )
                            govData.save()
                            print('okay works')
                            res = messages_sender(request,user)
                            print(res)
                            if res is True:
                                messages.success(request,'Your user account is already exsits! Check your email to activate the agency account!')
                                return redirect('sellerAgencyAccountSignup')
                            if res is False:
                                govData.delete()
                                messages.error(request,'Internal Problem Occured')
                                return redirect('sellerAgencyAccountSignup')
                else:
                    messages.warning(request,'Account already exsits! Check your email to activate the user account!')
                    return redirect('sellerAgencyAccountSignup')
            elif User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        messages.warning(request,'Your agency account is already exsits! Please login!')
                        return redirect('sellerAgencyAccountSignup')
                    else:
                        govData = GovId(
                        user=user,
                        govIdType=request.POST.get('govIdName'),
                        govIdNo = request.POST.get('govIdNo'),
                        govIdImage = request.FILES.get('govIdImage')
                        )
                        govData.save()
                        res = messages_sender(request,user)
                        print(res)
                        if res is True:
                            messages.success(request,'Your account is already exsits! Check your email to activate the agency account!')
                            return redirect('travelerAccountsSignup')
                        if res is False:
                            govData.delete()
                            messages.error(request,'Internal Problem Occured')
                            return redirect('travelerAccountsSignup')

                else:
                    messages.warning(request,'Account already exsits! Check your email to activate the user account!')
                    return redirect('sellerAgencyAccountSignup')
            elif User.objects.filter(phNo=phNo).exists():
                #print("gotcha1")
                user = User.objects.get(phNo=phNo)
                #print('gotcha2')
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        messages.warning(request,'Your agency account is already exsits! Please login!')
                        return redirect('sellerAgencyAccountSignup')
                    else:
                        govData = GovId(
                        user=user,
                        govIdType=request.POST.get('govIdName'),
                        govIdNo = request.POST.get('govIdNo'),
                        govIdImage = request.FILES.get('govIdImage')
                        )
                        govData.save()
                        res = messages_sender(request,user)
                        print(res)
                        if res is True:
                            messages.success(request,'Your account is already exsits! Check your email to activate the agency account!')
                            return redirect('travelerAccountsSignup')
                        if res is False:
                            govData.delete()
                            messages.error(request,'Internal Problem Occured')
                            return redirect('travelerAccountsSignup')

                else:
                    messages.warning(request,'Account already exsits! Check your email to activate the user account!')
                    return redirect('sellerAgencyAccountSignup')
            else:
                user = User(
                    name = request.POST.get('name'),
                    email=email,
                    phNo = phNo,
                    gender = request.POST.get('gender'),
                    DOB = request.POST.get('bdate'),
                    country = request.POST.get('country'),
                    state = request.POST.get('state'),
                    city = request.POST.get('city'),
                    address=request.POST.get('address'),
                    zipCode = request.POST.get('zip')
                )
                user.set_password(request.POST.get('password1'))
                user.is_active = False
                user.save()
                print("\n\n",request.POST.get('govIdName'),"\n")
                govData = GovId(
                    user=user,
                    govIdType=request.POST.get('govIdName'),
                    govIdNo = request.POST.get('govIdNo'),
                    govIdImage = request.FILES.get('govIdImage')
                )
                govData.save()

                res = messages_sender(request,user)
                print(res)
                if res is True:
                    messages.success(request,'Check your email to activate the account')
                    return redirect('sellerAgencyAccountSignup')
                if res is False:
                    user.delete()
                    messages.error(request,'Internal Problem Occured')
                    return redirect('sellerAgencyAccountSignup')
        except Exception as e:
            print("\n\n",e,"\n\n")
            messages.error(request,'Internal Problem Occured Exception')
            return redirect('sellerAgencyAccountSignup')
    else:
        return render(request,'accounts/seller_signup.html')




def agencyRegister(request):
    user = request.user
    if user.is_authenticated and request.session['access_type']=='seller':
        if user.userAccess.agency_access is True:
            if request.method == 'POST':
                agency = AgencyDetail(
                    user=user,
                    agencyName=request.POST.get('name'),
                    agency_Id = 'AGEN'+str(user.userAccess.agentId[4:]),
                    agencyPhNo=request.POST.get('phone'),
                    agencyCountry=request.POST.get('country'),
                    agencyCity=request.POST.get('city'),
                    agencyState=request.POST.get('state'),
                    agencyZipCode=request.POST.get('zip'),
                    govApproved=request.POST.get('govApproved'),
                    govApprovedId=request.POST.get('govApprovedId'),
                    agencyAddress=request.POST.get('agencyAddress')
                )
                agency.save()
                auth.logout(request)
                messages.success(request,'Agency Registered, Please wait till we verify your details, then you can add tours')
                return redirect('Seller_login')         
            else:
                return render(request,'registeragency.html')
        else:
            return redirect('Seller_login')
    else:
        messages.warning(request,'Please Login')
        return redirect('Seller_login')

        
   
# User Profile visiting
def userProfile(request, account_type, uid):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if (len(User.objects.filter(id=uid)) > 0):
                user = User.objects.get(id=uid)
                if user == request.user:
                    if account_type == 'traveller':
                        if user.userAccess.agency_access is True:
                            messages.error(request,"You can't change your details as you have a seller account")
                            return redirect(request.META.get('HTTP_REFERER'))
                        else:
                            user.name = request.POST.get('name')
                            user.DOB = request.POST.get('bdate')
                            user.phNo = request.POST.get('phone')
                            user.gender = request.POST.get('gender')
                            user.zipCode = request.POST.get('zip')
                            user.address = request.POST.get('address')
                            user.save()
                            messages.success(request, 'Successfully updated')
                            return redirect(request.META.get('HTTP_REFERER'))
                    elif account_type == 'seller':
                        return render(request,'forbidden.html')
                        # if request.POST.get('typo')=='agent':
                        #     user.name = request.POST.get('name')
                        #     user.DOB = request.POST.get('bdate')
                        #     user.phNo = request.POST.get('phone')
                        #     user.gender = request.POST.get('gender')
                        #     user.zipCode = request.POST.get('zip')
                        #     user.address = request.POST.get('address')
                        #     user.userGov.govIdType = request.POST.get('govIdName')
                        #     user.userGov.govIdNo = request.POST.get('govIdNo')
                        #     if(request.FILES.get('govIdImage')!=None):
                        #         user.userGov.govIdImage = request.FILES.get('govIdImage')
                        #     user.save()
                        #     user.userGov.save()
                        #     messages.success(request, 'Successfully updated')
                        #     return redirect(request.META.get('HTTP_REFERER'))
                        # elif request.POST.get('typo')=='agency':
                        #     user.userAgency.agencyName = request.POST.get('name')
                        #     user.userAgency.agencyPhNo = request.POST.get('phone')
                        #     user.userAgency.agencyAddress = request.POST.get('address')
                        #     user.userAgency.agencyZipCode = request.POST.get('zip')
                        #     user.userAgency.govApproved = request.POST.get('govApproved')
                        #     user.userAgency.govApprovedId = request.POST.get('govApprovedId')
                        #     user.userAgency.save()
                        #     messages.success(request, 'Successfully updated')
                        #     return redirect(request.META.get('HTTP_REFERER'))
                        # else:
                        #     return render(request,'forbidden.html')
                    else:
                        return render(request,'forbidden.html')
                else:
                    return render(request,'forbidden.html')
            else:
                return render(request,'forbidden.html')

        else:
            if (len(User.objects.filter(id=uid)) > 0):
                user = User.objects.get(id=uid)
                if user == request.user:
                    if account_type == 'traveller':
                        return render(request, 'accounts/travelleraccountedit.html')
                    elif account_type == 'seller':
                        return render(request, 'accounts/selleraccountedit.html')
                    else:
                        return render(request,'forbidden.html')
                else:
                    return render(request,'forbidden.html')
            else:
                return render(request,'forbidden.html')
    else:
        return render(request,'forbidden.html')

''' 
Author : Saptorshe
Purpose : Handling Password Change 
'''
def changePassword(request):
    if request.method == 'POST':
        oldpass = request.POST.get('oldpassword')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if check_password(oldpass,request.user.password):
            request.user.set_password(pass1)
            request.user.save()
            messages.success(request,'Successfully Changed your Password, please re-log in')
            return redirect('/')
        else:
             messages.error(request,'Enter your currect old password')
             return redirect(request.META.get('HTTP_REFERER'))        
    else:
        return render(request,'forbidden.html')
''' Password Chnage Function Ends Here '''




