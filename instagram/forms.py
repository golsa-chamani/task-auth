
from django.forms import Form, PasswordInput, TextInput, CharField,Textarea
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

class Bio(Form):
    new_bio = CharField(
    label="new_biography",
        max_length=150,
        required=True,
        widget=Textarea(attrs={
            "placeholder": "inter yor bio",
            "class": "form-control",
            "rows": 4
        })
    )
    def clean(self):
        bio = self.cleaned_data.get("new_bio")

        if "http" in bio.lower():
            raise ValidationError("bio does not have link")

        return bio
    


        