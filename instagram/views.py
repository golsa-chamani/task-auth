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







class GetBio(generic.View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        if not username:
            return render(request, "error.html", {
                "error_message": "Username is required."
            })

        instagram_key = uuid.uuid4()
        session_path =f'{settings.INSTAGRAM_SESSION_PATH}/{instagram_key}.json'
        
        if not os.path.exists(session_path):
            return render(request, "error.html", {
                "error_message": "Session file not found. Please login first."
            })

        try:
            cl = Client()
            cl.load_settings(session_path)
            cl.login(username, None)
            account = cl.account_info()

            return render(request, "intagram-profile.html", {
                "username": account.username,
                "bio": account.biography,
                "full_name": account.full_name
            })

        except Exception as e:
            return render(request, "error.html", {
                "error_message": f"Instagram error: {str(e)}"
            })





class EditBio(generic.FormView):
    template_name = 'instagram-editbio.html'
    form_class = forms.Bio
    success_url = reverse_lazy('instagram-profile')

    def get_instagram_client(self):
        username = self.request.session.get(settings.INSTAGRAM_SESSION_USERNAME)
        session_key = self.request.session.get(settings.INSTAGRAM_SESSION_KEY)
        
        if not username or not session_key:
            return None, ""

        session_path = f"{settings.INSTAGRAM_SESSION_PATH}/{session_key}.json"

        if not os.path.exists(session_path):
            return None, ""

        try:
            cl = Client()
            cl.load_settings(session_path)
            cl.login(username, None)
            return cl, None
        except Exception as e:
            return None, f"{e}"

    def form_valid(self, form):
        cl, error = self.get_instagram_client()

        if error:
            form.add_error(None, error)
            return self.form_invalid(form)

        new_bio = form.cleaned_data.get("new_bio")

        try:
            account = cl.account_info()

            cl.account_edit(
                biography=new_bio,
                external_url=account.external_url,
                gender=account.gender,
                email=account.email,
                phone_number=account.phone_number,
            )

            self.request.session['bio_update_success'] = True

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, f"{e}")
            return self.form_invalid(form)