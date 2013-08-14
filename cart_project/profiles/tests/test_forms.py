#-*- coding: utf-8 -*-

from django.test import TestCase
from profiles.models import StoreUser
from profiles.forms import (StoreUserCreationForm,
                            StoreUserUpdateForm,
                            StoreUserForm)


class StoreUserCreationFormTest(TestCase):
    def test_form_failure(self):
        # Missing field
        data = {"email": "testing@example.com",
                "password1": "pwd"}
        form = StoreUserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
                         {'password2': [u'This field is required.']})
        data.pop("email")
        form = StoreUserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
                         {'email': [u'This field is required.'],
                          'password2': [u'This field is required.']})
        # Password don't match
        data = {"email": "testing@example.com",
                "password1": "pwd", "password2": "pwdw"}
        form = StoreUserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
                         {'password2': [u"Passwords don't match"]})

    def test_form_success(self):
        data = {"email": "testing@example.com",
                "password1": "pwd", "password2": "pwd"}
        form = StoreUserCreationForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(StoreUser.objects.count(), 0)
        form.save()
        self.assertEqual(StoreUser.objects.count(), 1)
        user = StoreUser.objects.get(pk=1)
        self.assertTrue(user.is_staff)


class StoreUserUpdateFormTest(TestCase):
    def setUp(self):
        self.user = StoreUser.objects.create_merchant(
            "test@example.com",
            password="pwd"
        )

    def test_form_failure(self):
        # Empty data
        data = {"email": "", "last_login": self.user.last_login}
        form = StoreUserUpdateForm(data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
                         {'email': [u'This field is required.']})
        data.pop("last_login")
        form = StoreUserUpdateForm(data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,
                         {'email': [u'This field is required.'],
                          'last_login': [u'This field is required.']})

    def test_form_success(self):
        data = {"email": "testing2@example.com",
                "last_login": self.user.last_login}
        form = StoreUserUpdateForm(data, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(StoreUser.objects.count(), 1)
        form.save()
        self.assertEqual(StoreUser.objects.count(), 1)
        user = StoreUser.objects.get(pk=1)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, data['email'])
        # Lets add back the is_staff flag
        data.update({"is_staff": True})
        form = StoreUserUpdateForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(StoreUser.objects.count(), 1)
        user = StoreUser.objects.get(pk=1)
        self.assertTrue(user.is_staff)


class StoreUserFormTest(TestCase):
    # We are not testing the failure since we did already
    # for the StoreUserCreationForm
    def test_form_success(self):
        data = {"email": "testing@example.com",
                "password1": "pwd", "password2": "pwd"}
        form = StoreUserForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(StoreUser.objects.count(), 0)
        form.save()
        self.assertEqual(StoreUser.objects.count(), 1)
        user = StoreUser.objects.get(pk=1)
        self.assertFalse(user.is_staff)
