from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Email'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Confirm Password'
            })
        }


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


        from django import forms
from .models import Portfolio, PortfolioElement
from ckeditor.widgets import CKEditorWidget

from django import forms
from .models import Portfolio

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description']  # Exclude the 'user' field

class PortfolioElementForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = PortfolioElement
        fields = '__all__'


        # myApp/forms.py

from django import forms
from .models import AboutMe

class AboutMeForm(forms.ModelForm):
    class Meta:
        model = AboutMe
        fields = [
            'image',
            'name',
            'description',
            'background_nationality',
            'background_hometown',
            'background_languages',
            'skills',
            'education',
            'experience',
        ]