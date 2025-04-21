
from django.forms import Form, PasswordInput, TextInput, CharField
from django.core.exceptions import ValidationError



class Login(Form):
    username = CharField(label="", widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = CharField(label="", widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


    def clean(self):
        cleaned_data= super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username=='':
            raise ValidationError("please provide a username.")
        if password=='':
            raise ValidationError("please provide a password.")
        
        return cleaned_data

