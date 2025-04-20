from django.forms import Form, PasswordInput, TextInput, CharField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Signup(Form):
    username = CharField(label="", widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = CharField(label="", widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = CharField(label="", widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Retype your password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            return ValidationError('password not match')
        return password2

    def save(self):

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
        return user
