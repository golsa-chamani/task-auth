from django.views import generic
from . import forms


class SignupView(generic.FormView):
    form_class = forms.Signup
    template_name = 'registration/signup.html'
