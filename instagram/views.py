import os
from django.conf import settings
from instagrapi import Client
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from . import decorators
import uuid
from . import forms

@method_decorator(decorators.guest_required,name = 'dispatch')
class Login(generic.FormView):
    form_class = forms.Login
    template_name = 'instagram-login.html'
    success_url= reverse_lazy('instagram-profile')
    
    
    def form_valid(self,form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        instagram_key = uuid.uuid4()
        session_path =f'{settings.INSTAGRAM_SESSION_PATH}/{instagram_key}.json'
        



        try:
            cl = Client()
            cl.login(username, password)
            cl.dump_settings(session_path)
            request = self.request
            request.session[settings.INSTAGRAM_SESSION_KEY] = instagram_key
            request.session[settings.INSTAGRAM_SESSION_USERNAME] = username
            request.session[settings.INSTAGRAM_SESSION_ISLOGGEDIN] = True
            request.session.modified= True
            
            return super().form_valid(form)
        

        except Exception as e:
            form.add_error(None,f"Login to instagram failed: {e}")  
            return super().form_invalid(form)
   
@method_decorator(decorators.login_required,name = 'dispatch')
class Profile(generic.View):
    template_name = 'instagram-profile.html'

    
    def get(self,request):
        instagram_key =  request.session[settings.INSTAGRAM_SESSION_KEY] 
        session_path =f'{settings.INSTAGRAM_SESSION_PATH}/{instagram_key}.json'
        
        
        if os.path.exists(session_path):
            try:
                cl = Client()  
                cl.load_settings(session_path)
                return render(request,self.template_name)
                
            except Exception as e:
                del request.session[settings.INSTAGRAM_SESSION_KEY]
                del request.session[settings.INSTAGRAM_SESSION_USERNAME] 
                del request.session[settings.INSTAGRAM_SESSION_ISLOGGEDIN]
                request.session.modified= True
                print(f'faild to read session settings from {session_path}: {e}')
        return redirect(reverse('instagram-login'))


