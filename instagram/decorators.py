from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

def login_required(view_func):
    def wraper(request,*args,**kwargs):
        if not  request.session.get(settings.INSTAGRAM_SESSION_ISLOGGEDIN):
            return redirect(reverse('instagram-login'))
        return view_func(request,*args,**kwargs)
    return wraper





def guest_required(view_func):
    def wraper(request,*args,**kwargs):
        if request.session.get(settings.INSTAGRAM_SESSION_ISLOGGEDIN):
            return redirect(reverse('instagram-profile'))
        return view_func(request,*args,**kwargs)
    return wraper
