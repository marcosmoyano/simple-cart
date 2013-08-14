#-*- coding: utf-8 -*-

from django.test import TestCase
from stores.forms import AddToCartForm, UpdateCartForm


class AddToCartFormTest(TestCase):
    def test_form_failure(self):
        # Greater than 0
        data = {'quantity': 0}
        form = AddToCartForm(data)
        self.assertFalse(form.is_valid())
        # Whole numbers
        data = {'quantity': "hello"}
        form = AddToCartForm(data)
        self.assertFalse(form.is_valid())
        data = {'quantity': 1.1}
        form = AddToCartForm(data)
        self.assertFalse(form.is_valid())

    def test_form_success(self):
        data = {'quantity': 2}
        form = AddToCartForm(data)
        self.assertTrue(form.is_valid())


class UpdateCartFormTest(TestCase):
    def test_form_failure(self):
        # >= 0
        data = {'quantity': -1}
        form = UpdateCartForm(data)
        self.assertFalse(form.is_valid())
        # Whole numbers
        data = {'quantity': "hello"}
        form = UpdateCartForm(data)
        self.assertFalse(form.is_valid())
        data = {'quantity': 1.1}
        form = UpdateCartForm(data)
        self.assertFalse(form.is_valid())

    def test_form_success(self):
        # >= 0
        data = {'quantity': 0}
        form = UpdateCartForm(data)
        self.assertTrue(form.is_valid())
        data = {'quantity': 2}
        form = UpdateCartForm(data)
        self.assertTrue(form.is_valid())
