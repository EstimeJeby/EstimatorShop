from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from django.forms import ModelForm


class createUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
        widgets ={
            'username': forms.TextInput(attrs={'class': 'input '}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'password1': forms.PasswordInput(attrs={'class': 'input'}),
            'password2': forms.PasswordInput(attrs={'class': 'input'}),
            
        }
        
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets ={'username': forms.TextInput(attrs={'class':'input'}),
                  'email': forms.EmailInput(attrs={'class':'input'}),
                  
                  }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
        widgets ={
            'image': forms.FileInput(attrs={'class':'input'}),
            
        }
