#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import StoreUserCreationForm, StoreUserUpdateForm
from .models import StoreUser


__all__ = ['StoreUserAdmin', ]


class StoreUserAdmin(UserAdmin):
    add_form = StoreUserCreationForm
    form = StoreUserUpdateForm

    list_display = ("email", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser",
                   "is_active", "groups")
    search_fields = ("email", )
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active",
                                    "is_staff",
                                    "is_superuser",
                                    "groups",
                                    "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email",
                       "password1", "password2")}),
    )


admin.site.register(StoreUser, StoreUserAdmin)
