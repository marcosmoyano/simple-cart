#-*- coding: utf-8 -*-

from django.utils.timezone import now
from decimal import Decimal
from django.test import TestCase
from django.test.client import RequestFactory
from stores.models import Store, Product, Cart
from profiles.models import StoreUser
from stores.cart import UserCart

# More than testing our models we will be testing our UserCart
# wrapper to Store models


class UserCartTest(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = StoreUser.objects.create_user(
            "user@test.com", password="user"
        )
        merchant = StoreUser.objects.create_merchant(
            "test@test.com", password="test"
        )
        Store.objects.create(
            merchant=merchant,
            name="Testing", slug="testing"
        )
        Product.objects.create(
            store=Store.objects.get(pk=1),
            name="product 1", slug="product1",
            description="testing", price=Decimal(25)
        )

    def test_initialize_cart(self):
        request = self.request.get("/")
        request.user = self.user
        right_now = now()
        cart = UserCart(request)
        self.assertTrue(cart.is_empty())
        db_cart = Cart.objects.get(user=self.user, checked_out=False)
        self.assertTrue(cart.cart, db_cart)
        self.assertEqual(
            cart.cart.creation_date.timetuple()[:6],
            right_now.timetuple()[:6]
        )

    def test_add_cart(self):
        request = self.request.get("/")
        request.user = self.user
        cart = UserCart(request)
        self.assertTrue(cart.is_empty())
        product = Product.objects.get(slug="product1")
        cart.add(product, quantity=2)
        self.assertEqual(cart.cart.items.count(), 1)
        item = cart.cart.items.all()[0]
        self.assertEqual(cart.total(), Decimal(50))
        self.assertEqual(item.product, product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.total_price, Decimal(50))

    def test_update_cart(self):
        request = self.request.get("/")
        request.user = self.user
        cart = UserCart(request)
        self.assertTrue(cart.is_empty())
        product = Product.objects.get(slug="product1")
        cart.add(product, quantity=2)
        cart.update(product, quantity=4)
        self.assertEqual(cart.cart.items.count(), 1)
        item = cart.cart.items.all()[0]
        self.assertEqual(cart.total(), Decimal(100))
        self.assertEqual(item.product, product)
        self.assertEqual(item.quantity, 4)
        self.assertEqual(item.total_price, Decimal(100))
        # Lets remove all of them now and see what happens
        cart.update(product, quantity=0)
        self.assertEqual(cart.cart.items.count(), 0)
