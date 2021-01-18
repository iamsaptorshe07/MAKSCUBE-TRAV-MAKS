from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# User Model For registration ---------------------------------------------------------------------------
class UserManager(BaseUserManager):
    def create_user(self, email,password,name,DOB,gender,phNo, country,state,city,zipCode,address):
        """
        Creates and saves a User with the given email and password.
        """
        if not name:
            raise ValueError('User must have a Name')
        if not DOB:
            raise ValueError('User must have a Date of birth')
        if not phNo:
            raise ValueError('User must have a Phone Number')
        if not gender:
            raise ValueError('User must have a Gender')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('User must have a Password')
        if not country:
            raise ValueError('User must have a Country')
        if not state:
            raise ValueError('User must have a State')
        if not city:
            raise ValueError('User must have a City')
        if not zipCode:
            raise ValueError('User must have a Zip Code')
        if not address:
            raise ValueError('User must have an Address')

        user = self.model(
            email=self.normalize_email(email),
            phNo = phNo,
            name=name,
            DOB=DOB,
            gender=gender,
            country=country,
            state = state,
            city = city,
            zipCode = zipCode,
            address = address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password,phNo,name=None,DOB=None,gender=None, country=None,state=None,city=None,zipCode=None,address=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            phNo = phNo,
            password = password,
            name=name,
            DOB=DOB,
            gender=gender,
            country=country,
            state = state,
            city = city,
            zipCode = zipCode,
            address = address,
           
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    GENDER_CHOICE = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    name = models.CharField(max_length=100)
    DOB = models.DateField(null=False)
    phNo = models.BigIntegerField()
    gender = models.CharField(max_length=10,null=False, blank=False, choices = GENDER_CHOICE)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zipCode = models.BigIntegerField()
    address = models.CharField(max_length=100)

    
    creationTime = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','gender','DOB','phNo','country','state','city','zipCode','address']

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
# User Model Ends ---------------------------------------------------------------------------------------
    
# Phone verification model starts here ---------------------
class PhoneVerification(models.Model):    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phoneNo = models.BigIntegerField()
    verification = models.BooleanField(default=False)
# Phone verification model ends here ---------------------


# Account permission type starts here ------------------
class AccountType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userAccess')
    user_access = models.BooleanField(default=False)
    agency_access = models.BooleanField(default=False)
    guide_access = models.BooleanField(default=False)
    userId = models.CharField(max_length=50, unique=True, null=True, blank=True)
    agentId = models.CharField(max_length=50, unique=True, null=True, blank=True)
    guideId = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.email
    
    def get_user_Id(self):
        return self.userId

    def get_agent_Id(self):
        return self.agentId

    def get_guide_Id(self):
        return self.guideId
        

# Account permission type ends here ------------------

# GovId type starts here ------------------

class GovId(models.Model):
    GOV_CHOICE = (
        ('PAN','PAN'),
        ('ADHAR','ADHAR')
    ) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userGov')
    govIdType = models.CharField(max_length=10,choices = GOV_CHOICE)
    govIdNo = models.CharField(max_length=20)
    govIdImage = models.ImageField(upload_to='GovermentId_Proof')

# GovId type ends here ------------------

# Agency type starts here ------------------

class AgencyDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userAgency')
    agencyName = models.CharField(max_length=50)
    agency_logo = models.ImageField(null=True,blank=True)
    agency_Id = models.CharField(max_length=50)
    agencyPhNo = models.BigIntegerField()
    agencyCountry = models.CharField(max_length=25)
    agencyCity = models.CharField(max_length=20)
    agencyState = models.CharField(max_length=20)
    agencyZipCode = models.BigIntegerField()
    govApproved = models.BooleanField(default=False)
    govApprovedId = models.CharField(max_length=20,blank=True,null=True)
    agencyAddress = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    travmaks_partner = models.BooleanField(default=False)

    def __str__(self):
        return self.agencyName



# Agency type ends here ------------------

# Guide Service 
class GuideServiceArea(models.Model):
    area = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)

class GuideService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guideservice')
    service_area = models.ManyToManyField(GuideServiceArea)
    verified = models.BooleanField(default=False)