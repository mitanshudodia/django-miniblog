from django import forms
from .models import User
from django.core import validators

class Registration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','email','password']
        widgets = {
            'password' : forms.PasswordInput(attrs={'class':'form-control'},render_value=True),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
        }
