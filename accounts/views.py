# Import necesary libraries --------------------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.http import *
from .models import *
from .uniqueKey import *
from django.contrib import messages
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from .tokens import activation_token 
from django.utils.dateparse import parse_date
from django.conf import settings
from django.contrib.auth.hashers import check_password
#from django.template import RequestContext
# Importing ends here ---------------------

def messages_sender(request,user):
    try:
        check_access_target = str(request.get_full_path()).split('/')
        if check_access_target[2]=='traveller':
            email_temp = 'travellerMail'
        elif check_access_target[2]=='guide':
            email_temp = 'guideMail'
        elif check_access_target[2]=='seller':
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

def activateTraveller(request, uid, token):
    if len(User.objects.filter(id=uid))>0:
        user = User.objects.get(id=uid)
        if user is not None and activation_token.check_token(user,token):
            if user.is_active:
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
            return redirect('traveler_accounts_signup')
        else:
            return HttpResponse("Link Expired")
    else:
        return HttpResponse("ERROR 404")
    
# Traveller account creation and login page handler and also signup of traveller handler function ----
'''
This function is responsible for sending the account(Traveller / common user) creation and login page to the front - end and also 
responsible for handling the signup request of the user
'''
def travelerAccounts(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            phNo = request.POST.get('phone')
            print(email,phNo)
            if User.objects.filter(phNo=phNo,email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        messages.warning(request,'Your account is already exsits! Please login!')
                        return redirect('traveler_accounts_signup')
                    else:
                        res = messages_sender(request,user)
                        print(res)
                        if res is True:
                            messages.success(request,'As your seller account already exists we will use your old data just Check your email to activate the user account')
                            return redirect('traveler_accounts_signup')
                        if res is False:
                            messages.error(request,'Internal Problem Occured')
                            return redirect('traveler_accounts_signup')
                else:
                    messages.warning(request,'Account already exsits! Please verify your email! sent on {}'.format(user.creationTime))
                    return redirect('traveler_accounts_signup')
            elif User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        messages.warning(request,'Your account is already exsits! Please login!')
                        return redirect('traveler_accounts_signup')
                    else:
                        res = messages_sender(request,user)
                        print(res)
                        if res is True:
                            messages.success(request,'As your seller account already exists we will use your old data just Check your email to activate the user account')
                            return redirect('traveler_accounts_signup')
                        if res is False:
                            messages.error(request,'Internal Problem Occured')
                            return redirect('traveler_accounts_signup')
                        return redirect('travelAgency_accounts_signup')
                else:
                    messages.warning(request,'Account already exsits! Please verify your email! sent on {}'.format(user.creationTime))
                    return redirect('traveler_accounts_signup')
            elif User.objects.filter(phNo=phNo).exists():
                user = User.objects.get(phNo=phNo)
                if user.is_active:
                    if user.userAccess.user_access is True:
                        messages.warning(request,'Your account is already exsits! Please login!')
                        return redirect('traveler_accounts_signup')
                    else:
                        messages.warning(request,'Agency account already exsits! Check your email to activate the user account!')
                        
                        return redirect('travelAgency_accounts_signup')
                else:
                    messages.warning(request,'Account already exsits! Please verify your email!')
                    return redirect('traveler_accounts_signup')
            else:
                user = User(
                    name = request.POST.get('name'),
                    email=email,
                    gender = request.POST.get('gender'),
                    DOB = request.POST.get('bdate'),
                    phNo = request.POST.get('phone'),
                    country = request.POST.get('country'),
                    state = request.POST.get('state'),
                    city = request.POST.get('city'),
                    address=request.POST.get('address'),
                    zipCode = request.POST.get('zip')
                )
                user.set_password(request.POST.get('password1'))
                user.is_active = False
                user.save()
                res = messages_sender(request,user)
                print(res)
                if res is True:
                    messages.success(request,' email to activatCheck youre the account')
                    return redirect('traveler_accounts_signup')
                if res is False:
                    messages.error(request,'Internal Problem Occured')
                    return redirect('traveler_accounts_signup')
        except Exception as e:
            print(e)
            return redirect('/')
    else:
        return render(request,'travelleraccounts.html')

# Traveller signup and account page handler ends here -------------------------------------------

# Traveller Login handler Starts here ----------------------------------------
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
                            return redirect('traveler_accounts_signup')
                    else:
                        messages.warning(request,"You don't have any user account, Please register yourself as an user")
                        return redirect('traveler_accounts_signup')
                else:
                    messages.warning(request,'Check your mail sent on {}'.format(user.creationTime))
                    return redirect('/')
            else:
                messages.error(request,"Please Signup before Login")
                return redirect('traveler_accounts_signup')
        except Exception as problem:
            messages.warning(request, problem)
            return redirect('traveler_accounts_signup')
    else:
        return HttpResponse("404 BAD REQUEST")
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
                            auth.login(request,user)
                            request.session['access_type']='seller'
                            messages.success(request,'Successfully Loggedin')
                            return redirect('/')
                        else:
                            messages.error(request,'Invalid Credential')
                            return redirect('travelAgency_accounts_signup')
                    else:
                        messages.warning(request,"You don't have any agency account, Please register yourself as an user")
                        return redirect('travelAgency_accounts_signup')
                else:
                    messages.warning(request,'Check your mail sent on {} to activate the account'.format(user.creationTime))
                    return redirect('/')
            else:
                messages.error(request,"Please Signup before Login")
                return redirect('travelAgency_accounts_signup')
        except Exception as problem:
            messages.warning(request, problem)
            return redirect('travelAgency_accounts_signup')
    else:
        return HttpResponse("404 BAD REQUEST")
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
'''
This function is responsible for sending the account(Seller - Agency and guide) creation and login page to the front - end and also 
responsible for handling the signup request of the sellers (Travel agency not guide)
'''
def activateSeller(request, uid, token):
    user = User.objects.get(id=uid)
    if user is not None and activation_token.check_token(user,token):
        messages.success(request,'Please complete your profile!')
        return render(request,'registeragency.html',{'id':uid})
    else:
        return HttpResponse("Forbidden")
    

def sellerAgencyAccount(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            phNo = request.POST.get('phone')
            print(request.POST.get('govIdName'))
            print(email,phNo)
            if User.objects.filter(phNo=phNo,email=email).exists():
            #if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        messages.warning(request,'Your agency account is already exsits! Please login!')
                        return redirect('travelAgency_accounts_signup')
                    else:

                        if GovId.objects.filter(user=user).exists():
                            messages.warning(request,'Agency account verification mail has been send! Please verify your self!')
                            return redirect('travelAgency_accounts_signup')
                        else:
                            print('okay works1233')
                            #print(request.POST.get('govIdName'))
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
                                return redirect('traveler_accounts_signup')
                            if res is False:
                                messages.error(request,'Internal Problem Occured')
                                return redirect('traveler_accounts_signup')
                else:
                    messages.warning(request,'Account already exsits! Check your email to activate the user account!')
                    return redirect('travelAgency_accounts_signup')
            elif User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        messages.warning(request,'Your agency account is already exsits! Please login!')
                        return redirect('travelAgency_accounts_signup')
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
                            return redirect('traveler_accounts_signup')
                        if res is False:
                            messages.error(request,'Internal Problem Occured')
                            return redirect('traveler_accounts_signup')
                        return redirect('traveler_accounts_signup')
                else:
                    messages.warning(request,'Account already exsits! Check your email to activate the user account!')
                    return redirect('travelAgency_accounts_signup')
            elif User.objects.filter(phNo=phNo).exists():
                #print("gotcha1")
                user = User.objects.get(phNo=phNo)
                #print('gotcha2')
                if user.is_active:
                    if user.userAccess.agency_access is True:
                        messages.warning(request,'Your agency account is already exsits! Please login!')
                        return redirect('travelAgency_accounts_signup')
                    else:
                        messages.warning(request,'Your account is already exsits! Please login!')
                        return redirect('traveler_accounts_signup')
                else:
                    messages.warning(request,'Account already exsits! Check your email to activate the user account!')
                    return redirect('travelAgency_accounts_signup')
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
                    return redirect('travelAgency_accounts_signup')
                if res is False:
                    messages.error(request,'Internal Problem Occured')
                    return redirect('travelAgency_accounts_signup')
        except Exception as e:
            print("\n\n",e,"\n\n")
            messages.error(request,'Internal Problem Occured Exception')
            return redirect('travelAgency_accounts_signup')
    else:
        return render(request,'selleraccount.html')

# Traveller signup and account page handler ends here -------------------------------------------

# Handles a signup request of a guide --------
def sellerGuideSignup(request):
    pass 
# Signup request of guide ends here


# Handle login request ofa guide ----
def sellerGuideLogin(request):
    pass
# Guide login request handler ends here ---



def agencyRegister(request,id):
    if request.method == 'POST':
        try:
            if User.objects.filter(id=id).exists():
                user = User.objects.get(id=id)
                if user.is_active:
                    access = AccountType.objects.get(user=user)
                    access.agency_access=True
                    access.agentId=sellerId()
                else:
                    access =AccountType(user=user,agency_access=True,agentId=sellerId())
                    user.is_active = True
                access.save()
                access_user = AccountType.objects.get(user=user)
                agency = AgencyDetail(
                    user=user,
                    agencyName=request.POST.get('name'),
                    agency_Id = 'AGEN'+str(access_user.agentId[4:]),
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
                user.save()
                messages.success(request,'Successfully registered')
                return redirect('travelAgency_accounts_signup')
        except Exception as e:
            print(e)
            messages.error(request,e)
            return redirect('travelAgency_accounts_signup')
    else:
        return render(request,'registeragency.html')


def userProfile(request, account_type, uid):
    if request.method == 'POST':
        if (len(User.objects.filter(id=uid)) > 0):
            user = User.objects.get(id=uid)
            if user == request.user:
                if account_type == 'traveller':
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
                    if request.POST.get('typo')=='agent':
                        user.name = request.POST.get('name')
                        user.DOB = request.POST.get('bdate')
                        user.phNo = request.POST.get('phone')
                        user.gender = request.POST.get('gender')
                        user.zipCode = request.POST.get('zip')
                        user.address = request.POST.get('address')
                        user.userGov.govIdType = request.POST.get('govIdName')
                        user.userGov.govIdNo = request.POST.get('govIdNo')
                        if(request.FILES.get('govIdImage')!=None):
                            user.userGov.govIdImage = request.FILES.get('govIdImage')
                        user.save()
                        user.userGov.save()
                        messages.success(request, 'Successfully updated')
                        return redirect(request.META.get('HTTP_REFERER'))
                    elif request.POST.get('typo')=='agency':
                        user.userAgency.agencyName = request.POST.get('name')
                        user.userAgency.agencyPhNo = request.POST.get('phone')
                        user.userAgency.agencyAddress = request.POST.get('address')
                        user.userAgency.agencyZipCode = request.POST.get('zip')
                        user.userAgency.govApproved = request.POST.get('govApproved')
                        user.userAgency.govApprovedId = request.POST.get('govApprovedId')
                        user.userAgency.save()
                        messages.success(request, 'Successfully updated')
                        return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        return HttpResponse("BAD REQUEST")
                else:
                    return HttpResponse("BAD REQUEST")
            else:
                return HttpResponse("BAD REQUEST")
        else:
            return HttpResponse("BAD REQUEST")

    else:
        if (len(User.objects.filter(id=uid)) > 0):
            user = User.objects.get(id=uid)
            if user == request.user:
                if account_type == 'traveller':
                    return render(request, 'accounts/travelleraccountedit.html')
                elif account_type == 'seller':
                    return render(request, 'accounts/selleraccountedit.html')
                else:
                    return HttpResponse("BAD REQUEST")
            else:
                return HttpResponse("BAD REQUEST")
        else:
            return HttpResponse("BAD REQUEST")

def reset_messages_sender(request,user):
    try:
        site = get_current_site(request)
        mail_subject = 'Site Activation Link'
        message = render_to_string('resetMail.html', {
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

def userValidation(request, uid, token):
    if len(User.objects.filter(id=uid))>0:
        user = User.objects.get(id=uid)
        if user is not None and activation_token.check_token(user,token):
            if request.method == 'GET':
                context={'user': user,'token':token}
                responce = render(request, 'accounts/changePassword.html',context=context)
                responce.set_cookie('uid',uid,max_age=None)
                return responce
            else:
                uid_check = request.COOKIES.get('uid')
                if uid_check == uid:
                    pass1 = request.POST.get('password1')
                    user.set_password(pass1)
                    user.save()
                    x=activation_token.make_token(user)
                    print("\n\n")
                    print(x)
                    responce = redirect('traveler_accounts_signup')
                    responce.delete_cookie('uid')
                    messages.success(request,'Successfully Changed your Password, please re-log in')
                    return responce    
                else:
                    return HttpResponse("BAD REQUEST")
        else:
            return HttpResponse("Link Expired")
    else:
        return HttpResponse("ERROR 404")
    


def passwordReset(request):
    if request.method == 'GET':
        return render(request, 'accounts/passwordChange.html')
    else:
        mail = request.POST.get('email')
        if User.objects.filter(email=mail).exists():
            user = User.objects.get(email=mail)
            if user.is_active:
                res = reset_messages_sender(request,user)
                print(res)
                if res is True:
                    messages.success(request,'Check your mail inbox')
                    return redirect('traveler_accounts_signup')
                if res is False:
                    messages.error(request,'Internal Problem Occured')
                    return redirect('traveler_accounts_signup')
            else:
                messages.error(request,'Please varify your mail frist')
                return redirect('traveler_accounts_signup')
        else:
            messages.error(request,'Enter a valid mail-id')
            return redirect('traveler_accounts_signup')

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
        return HttpResponse("BAD REQUEST")