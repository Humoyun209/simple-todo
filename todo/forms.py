import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Todo
from django import forms
from django.contrib.auth.models import User


class CreateToDo(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('name', 'memo', 'important')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match('\d', name):
            raise ValidationError('The name cannot start with letters')
        return name

    def clean_content(self):
        content = self.cleaned_data['memo']
        if len(content) < 5:
            raise ValidationError('The memo Length < 5')
        return content

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='Name',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(max_length=12, label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password2 = forms.CharField(max_length=12, label='Password(again)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.CharField(max_length=255, label='Email',
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(max_length=15, label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

