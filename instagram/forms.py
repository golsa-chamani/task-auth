from django.forms import Form, PasswordInput, TextInput, CharField, Textarea
from django.core.exceptions import ValidationError
from . import models


class Login(Form):
    username = CharField(
        label="",
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = CharField(
        label="",
        widget=PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username == "":
            raise ValidationError("please provide a username.")
        if password == "":
            raise ValidationError("please provide a password.")

        return cleaned_data


class ProfileEdit(Form):
    bio = CharField(
        label="",
        max_length=1024,
        required=True,
        widget=Textarea(
            attrs={
                "placeholder": "Biography",
                "class": "form-control",
                "rows": 18,
                "cols": 64,
            }
        ),
    )

    full_name = CharField(
        label="",
        max_length=64,
        required=True,
        widget=TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Full Name",
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        bio = kwargs.pop("bio", None)
        full_name = kwargs.pop("full_name", None)
        super().__init__(*args, **kwargs)
        self.fields["bio"].initial = bio
        self.fields["full_name"].initial = full_name

    def clean_bio(self):
        bio = self.cleaned_data.get("bio")
        if "http" in bio.lower():
            raise ValidationError("bio should not have link")
        return bio

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        return full_name
