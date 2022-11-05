from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Prediction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileRegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

class contestEntryForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['temp1',
                  'temp2',
                  'coverage']
        if User.is_authenticated:
            Prediction.source = User


