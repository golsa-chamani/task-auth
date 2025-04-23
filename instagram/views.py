import os
from django.conf import settings
from instagrapi import Client
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from . import decorators
import uuid
from . import forms


@method_decorator(decorators.guest_required, name="dispatch")
class Login(generic.FormView):
    form_class = forms.Login
    template_name = "instagram-login.html"
    success_url = reverse_lazy("instagram-profile")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        instagram_key = str(uuid.uuid4())
        session_path = f"{settings.INSTAGRAM_SESSION_PATH}/{instagram_key}.json"

        try:
            cl = Client()
            cl.login(username, password)
            cl.dump_settings(session_path)
            request = self.request
            request.session[settings.INSTAGRAM_SESSION_KEY] = instagram_key
            request.session.modified = True
            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, f"Login to instagram failed: {e}")
            return super().form_invalid(form)


class Logout(generic.View):
    def get(self, request):
        if hasattr(request, 'instagram_client'):
            cl = request.instagram_client
            cl.logout()
        instagram_key = request.session.get(settings.INSTAGRAM_SESSION_KEY)
        if instagram_key:
            del request.session[settings.INSTAGRAM_SESSION_KEY]
            request.session.modified = True
            session_path = f"{settings.INSTAGRAM_SESSION_PATH}/{instagram_key}.json"
            try:
                os.remove(session_path)
            except Exception as e:
                print(
                    f"exception occured while trying to delete user instagram session settings at {session_path}: {e}"
                )
        return redirect(reverse("instagram-login"))


@method_decorator(decorators.login_required, name="dispatch")
class Profile(generic.View):
    template_name = "instagram-profile.html"

    def get(self, request):
        cl = request.instagram_client
        account = cl.account_info()
        ctx = {
            "username": account.username,
            "bio": account.biography,
            "full_name": account.full_name,
        }
        return render(request, self.template_name, context=ctx)


@method_decorator(decorators.login_required, name="dispatch")
class ProfileEdit(generic.FormView):
    form_class = forms.ProfileEdit
    template_name = "instagram-profile-edit.html"
    success_url = reverse_lazy("instagram-profile")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        request = self.request
        cl = request.instagram_client
        account = cl.account_info()
        account_info = {
            "bio": account.biography,
            "full_name": account.full_name,
        }
        kwargs.update({"account_info": account_info})

        return kwargs

    def form_valid(self, form):
        bio = form.cleaned_data.get("bio")
        full_name = form.cleaned_data.get("full_name")
        try:
            request = self.request
            cl = request.instagram_client
            cl.account_edit(biography=bio, full_name=full_name)
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, f"{e}")
            return self.form_invalid(form)
