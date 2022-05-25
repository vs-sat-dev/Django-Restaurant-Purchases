from django import forms
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator


User = get_user_model()


class RegisterForm(UserCreationForm):
    username = forms.CharField(validators=[
                                   RegexValidator(regex=r'^[a-zA-Z]{1}[a-zA-Z0-9_\-]*',
                                                  message='Username must start with letters and contain only letters, '
                                                          'numbers, hyphens, or the underscore character when creating '
                                                          'a new user'),
                                   MinLengthValidator(3, message='Username must contain at least 3 symbols'),
                                   MaxLengthValidator(32, message='Username must be less or equal to 32 symbols')
                               ],
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=128,
                             validators=[EmailValidator],
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(validators=[
        MinLengthValidator(8, message='Password must contain at least 8 symbols'),
        MaxLengthValidator(32, message='Password must be less or equal to 32 symbols')
        ],
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(validators=[
        MinLengthValidator(8, message='Password must contain at least 8 symbols'),
        MaxLengthValidator(32, message='Password must be less or equal to 32 symbols')
        ],
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=32,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')
