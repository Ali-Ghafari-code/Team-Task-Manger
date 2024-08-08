from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import validators
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(100)]
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
       ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('Passwords are not match')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control', ' id': 'exampleInputEmail1'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه ی عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه ی عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

