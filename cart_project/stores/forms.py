#-*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _


__all__ = ['AddToCartForm', 'UpdateCartForm']


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(label=_("Quantity"),
                                  initial=1, min_value=1)


class UpdateCartForm(forms.Form):
    quantity = forms.IntegerField(label=_("Quantity"),
                                  min_value=0)
