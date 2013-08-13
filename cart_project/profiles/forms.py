#-*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import StoreUser


__all__ = ['StoreUserCreationForm', 'StoreUserUpdateForm', 'StoreUserForm']


class StoreUserCreationForm(forms.ModelForm):
    """ A form for creating Merchant Users """
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput)

    class Meta:
        model = StoreUser
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(StoreUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user


class StoreUserUpdateForm(forms.ModelForm):
    """ A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin"s password hash display field.  """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = StoreUser

    def clean_password(self):
        # Regardless of what the user provides, return the
        # initial value. This is done here, rather than on
        # the field, because the field does not have access
        # to the initial value
        return self.initial["password"]


class StoreUserForm(StoreUserCreationForm):
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(StoreUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = False
        if commit:
            user.save()
        return user
