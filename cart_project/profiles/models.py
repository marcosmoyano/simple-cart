#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
BaseUserManager, AbstractBaseUser, PermissionsMixin
)


__all__ = ['StoreUser', ]


class StoreUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the . given email and
        password.
        """
        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)
        user = self.model(
            email=StoreUserManager.normalize_email(email),
            is_active=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_merchant(self, email, password=None):
        """
        Creates and saves a Merchant with the . given email and
        password.
        """
        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)
        user = self.model(
            email=StoreUserManager.normalize_email(email),
            is_active=True
        )
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Creates and saves a superuser with the given email
        and password.  """
        user = self.create_user(email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class StoreUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email address"), max_length=255,
                              unique=True,
                              db_index=True)
    USERNAME_FIELD = "email"
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = StoreUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email
