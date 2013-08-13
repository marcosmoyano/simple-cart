#-*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from stores.cart import UserCart
from .forms import StoreUserForm


@login_required
def checkout(request, template="profiles/checkout.html"):
    cart = UserCart(request)
    if request.method == "POST":
        cart.checkout()
        messages.info(request, 'Your cart has been processed')
        return HttpResponseRedirect(reverse("stores:home"))
    return render(request, template, {
        'cart': cart,
        'empty': cart.is_empty(),
    })


def register(request, template="registration/register.html"):
    if request.user.is_authenticated():
        messages.info(request, "You are logged in already")
        return HttpResponseRedirect(reverse("stores:home"))
    form = StoreUserForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user = authenticate(username=user.email,
                            password=form.cleaned_data.get('password1'))
        login(request, user)
        messages.info(request, "Your registration has been completed")
        return HttpResponseRedirect(reverse("stores:home"))
    return render(request, template, {"form": form})
