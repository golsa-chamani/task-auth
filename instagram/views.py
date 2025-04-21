import os
from django.conf import settings
from instagrapi import Client
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from . import forms


class Login(generic.FormView):
    form_class = forms.Login
    template_name = 'instagram-login.html'
    success_url= reverse_lazy('instagram-profile')
    
    def form_valid(self,form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        cl = Client()
        session_path = settings.INSTAGRAM_SESSION_PATH

        if os.path.exists(session_path):
            try:
                cl.load_settings(session_path)
            except Exception as e:
                print(f'faild to read session settings from {session_path}: {e}')

        try:  
            cl.login(username, password)
            cl.dump_settings(session_path)
            return super().form_valid(form)

        except Exception as e:
            form.add_error(None,f"Login to instagram failed: {e}")  
            return self.form_invalid(form)   
    
class Profile(generic.View):
    template_name = 'instagram-profile.html'

    
    def get(self,request):
        return render(request,self.template_name)


