from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from instagrapi import Client


def login_required(view_func):
    def wraper(request, *args, **kwargs):
        instagram_key = request.session[settings.INSTAGRAM_SESSION_KEY]
        session_path = f"{settings.INSTAGRAM_SESSION_PATH}/{instagram_key}.json"
        try:
            cl = Client()
            cl.load_settings(session_path)
            setattr(request, 'instagram_client', cl)
        except Exception as e:
            return redirect(reverse("instagram-logout"))
        return view_func(request, *args, **kwargs)

    return wraper


def guest_required(view_func):
    def wraper(request, *args, **kwargs):
        if request.session.get(settings.INSTAGRAM_SESSION_KEY):
            return redirect(reverse("instagram-profile"))
        return view_func(request, *args, **kwargs)

    return wraper
