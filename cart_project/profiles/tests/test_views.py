#-*- coding: utf-8 -*-

from decimal import Decimal
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from profiles.models import StoreUser
from profiles.forms import StoreUserForm
from stores.models import Store, Product, Cart
from stores.cart import UserCart


class CheckoutTest(TestCase):
    # Since we don't have a payment process
    # we only check for GET vs POST
    def setUp(self):
        merchant = StoreUser.objects.create_merchant(
            "test@test.com", password="test"
        )
        self.request = RequestFactory()
        self.user = StoreUser.objects.create_user("user@test.com", "user")
        Store.objects.create(merchant=merchant,
                             name="Testing", slug="testing")
        Store.objects.create(merchant=merchant,
                             name="Testing2", slug="testing2")
        Product.objects.create(store=Store.objects.get(pk=1),
                               name="product 1", slug="product1",
                               description="testing", price=Decimal(25))
        Product.objects.create(store=Store.objects.get(pk=2),
                               name="product 2", slug="product2",
                               description="testing 2", price=Decimal(35))
        self.client = Client()

    def test_checkout_get(self):
        self.client.login(email=self.user.email, password="user")
        response = self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('checkout'))
        self.assertFalse(response.context['empty'])
        request = self.request.get("/")
        request.user = self.user
        cart = UserCart(request)
        self.assertEqual(response.context['cart'].cart, cart.cart)

    def test_checkout_post(self):
        self.client.login(email=self.user.email, password="user")
        response = self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        request = self.request.get("/")
        request.user = self.user
        cart1 = UserCart(request)
        self.assertEqual(cart1.cart.items.count(), 1)
        response = self.client.post(reverse('checkout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))
        # The Cart should be gone and a new one should be created
        request = self.request.get("/")
        request.user = self.user
        cart2 = UserCart(request)
        self.assertEqual(cart2.cart.items.count(), 0)
        self.assertNotEqual(cart1.cart.creation_date, cart2.cart.creation_date)
        # Even more, lets check the pk
        self.assertNotEqual(cart1.cart.pk, cart2.cart.pk)


class PastOrdersTest(TestCase):
    def setUp(self):
        merchant = StoreUser.objects.create_merchant(
            "test@test.com", password="test"
        )
        self.request = RequestFactory()
        self.user = StoreUser.objects.create_user("user@test.com", "user")
        Store.objects.create(merchant=merchant,
                             name="Testing", slug="testing")
        Store.objects.create(merchant=merchant,
                             name="Testing2", slug="testing2")
        Product.objects.create(store=Store.objects.get(pk=1),
                               name="product 1", slug="product1",
                               description="testing", price=Decimal(25))
        Product.objects.create(store=Store.objects.get(pk=2),
                               name="product 2", slug="product2",
                               description="testing 2", price=Decimal(35))
        self.client = Client()

    def test_past_orders_get(self):
        self.client.login(email=self.user.email, password="user")
        self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)
        self.client.post(reverse('checkout'), follow=True)
        response = self.client.get(reverse('past_orders'))
        carts = Cart.objects.filter(user=self.user, checked_out=True)
        self.assertEqual(carts.count(), 1)
        self.assertEqual(list(carts), list(response.context['carts']))


class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_failure(self):
        data = {'email': 'test@example.com',
                'password1': 'pwd',
                'password2': "pwdw"}

        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        # Lets make sure we get an empty form
        form = StoreUserForm()
        self.assertEqual(response.context['form'].is_bound, form.is_bound)
        self.assertEqual(response.context['form'].initial, form.initial)
        self.assertEqual(response.context['form'].data, form.data)
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            [u"Passwords don't match"]
        )
        data.pop("password2")
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            [u"This field is required."]
        )

    def test_success(self):
        data = {'email': 'test@example.com',
                'password1': 'pwd',
                'password2': "pwd"}
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(StoreUser.objects.count(), 1)
        user = StoreUser.objects.get(pk=1)
        self.assertEqual(user.email, data['email'])
