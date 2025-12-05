from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if not email.endswith('@gmail.com'):
            raise ValidationError("Email must end with @gmail.com")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists — please use another email")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists — please choose a different username")
        return username