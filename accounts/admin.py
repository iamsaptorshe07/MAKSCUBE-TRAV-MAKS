from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name','email','gender','DOB','phNo','country','state','city','zipCode','address')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
  
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('name','email','DOB','phNo', 'password', 'gender','country','state','city','zipCode','address','is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name','email','DOB','phNo', 'gender','country','state','city','zipCode','address','creationTime', 'is_admin','is_superuser','is_active')
    list_filter = ('is_admin','is_superuser','is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','phNo','gender','DOB','country','state','city','zipCode','address')}),
        ('Permissions', {'fields': ('is_admin','is_superuser','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','email','phNo','DOB','gender','country','state','city','zipCode','address','password1','password2')}
        ),
    )
    search_fields = ('email','phNo')
    ordering = ('email',)
    filter_horizontal = ()



    
class AccountTypeAdmin(admin.ModelAdmin):
    model = AccountType
    list_display = ('user','user_access','guide_access','agency_access','userId','agentId','guideId')
    search_fields = ['user__email','userId','guideId','agentId']
    list_filter = ('user_access','guide_access','agency_access')


class GovtIdAdmin(admin.ModelAdmin):
    model = GovId
    list_display = ('user','govIdType','govIdNo','govIdImage')
    search_fields = ['user__email','govIdNo']
    list_filter = ('govIdType',)


class AgencyDetailsAdmin(admin.ModelAdmin):
    model = AgencyDetail
    list_display = ('agencyName','user','agency_Id','agencyPhNo','agencyCountry','agencyCity','agencyState','agencyZipCode','agencyAddress','govApproved','govApprovedId','verified','travmaks_partner')
    search_fields = ['user__email','agencyName','govApprovedId','agencyPhNo','agency_Id']
    list_filter = ('govApproved','agencyCountry','travmaks_partner','verified')

    
# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(PhoneVerification)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(GovId,GovtIdAdmin)
admin.site.register(AgencyDetail, AgencyDetailsAdmin)
admin.site.register(GuideServiceArea)
admin.site.register(GuideService)