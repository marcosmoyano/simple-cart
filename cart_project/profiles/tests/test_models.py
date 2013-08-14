#-*- coding: utf-8 -*-

from django.test import TestCase
from profiles.models import StoreUser


class StoreUserManagerTest(TestCase):
    def test_failure(self):
        # missing email
        self.assertRaises(
            TypeError,
            StoreUser.objects.create_user, password="pwd"
        )
        self.assertRaises(
            TypeError,
            StoreUser.objects.create_merchant, password="pwd"
        )
        self.assertRaises(
            TypeError,
            StoreUser.objects.create_superuser, password="pwd"
        )

    def test_success(self):
        user = StoreUser.objects.create_user(
            "test1@example.com",
            password="pwd"
        )
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(StoreUser.objects.count(), 1)

        merchant = StoreUser.objects.create_merchant(
            "merchant@example.com",
            password="pwd"
        )
        self.assertTrue(merchant.is_staff)
        self.assertFalse(merchant.is_superuser)
        self.assertEqual(StoreUser.objects.count(), 2)
        admin = StoreUser.objects.create_superuser(
            "admin@example.com",
            password="pwd"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(StoreUser.objects.count(), 3)
