#-*- coding: utf-8 -*-

from decimal import Decimal
from django.test import TestCase
from django.test.client import Client
from stores.models import Store, Product, Cart, Item
from profiles.models import StoreUser
from django.core.urlresolvers import reverse


class StoreTest(TestCase):
    def setUp(self):
        merchant = StoreUser.objects.create_merchant(
            "test@test.com", password="test"
        )
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

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(list(response.context['stores']),
                         list(Store.objects.all()))

    def test_store(self):
        response = self.client.get(reverse('stores:store',
                                           kwargs={'slug': 'testing'}))
        store = Store.objects.get(slug="testing")
        self.assertEqual(response.context['store'], store)
        self.assertEqual(list(response.context['products']),
                         list(store.product_set.all()))
        response = self.client.get(reverse('stores:store',
                                           kwargs={'slug': 'testing2'}))
        store2 = Store.objects.get(slug="testing2")
        self.assertEqual(response.context['store'], store2)
        self.assertEqual(list(response.context['products']),
                         list(store2.product_set.all()))

    def test_add_to_cart_success(self):
        self.client.login(email=self.user.email, password="user")
        response = self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('stores:store', kwargs={
            "slug": "testing",
        }))
        cart = Cart.objects.get(user=self.user, checked_out=False)
        product = Product.objects.get(slug="product1")
        item = Item.objects.get(cart=cart, product=product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.total_price, Decimal(50))

    def test_add_to_cart_not_logged_in(self):
        response = self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        next = reverse('login') + "?next=" + reverse(
            'stores:add_to_cart', kwargs={
                "store_slug": "testing",
                "slug": "product1"
            })
        self.assertRedirects(response, next)

    def test_add_to_cart_failure(self):
        self.client.login(email=self.user.email, password="user")
        response = self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 0}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "quantity",
            [u'Ensure this value is greater than or equal to 1.']
        )

    def test_update_cart_success(self):
        self.client.login(email=self.user.email, password="user")
        # Lets create a Cart First
        response = self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)
        # Now let's update it
        response = self.client.post(reverse('stores:update_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 4}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('checkout'))
        cart = Cart.objects.get(user=self.user, checked_out=False)
        product = Product.objects.get(slug="product1")
        item = Item.objects.get(cart=cart, product=product)
        self.assertEqual(item.quantity, 4)
        self.assertEqual(item.total_price, Decimal(100))

    def test_update_cart_not_logged_in(self):
        response = self.client.post(reverse('stores:update_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)
        self.assertEqual(response.status_code, 200)
        next = reverse('login') + "?next=" + reverse(
            'stores:update_cart', kwargs={
                "store_slug": "testing",
                "slug": "product1"
            })
        self.assertRedirects(response, next)

    def test_update_cart_failure(self):
        self.client.login(email=self.user.email, password="user")
        response = self.client.post(reverse('stores:add_to_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": 2}, follow=True)

        response = self.client.post(reverse('stores:update_cart', kwargs={
            "store_slug": "testing",
            "slug": "product1"
        }), {"quantity": "hello"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "quantity",
            [u'Enter a whole number.']
        )
