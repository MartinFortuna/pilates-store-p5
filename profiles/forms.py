from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserDetail


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=25,
        label="First Name",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
            }
        )
    )
    last_name = forms.CharField(
        max_length=25,
        label="Last Name",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {
            'username': None,
            'password': None,
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = UserDetail
        fields = ['telephone', 'address1', 'address2', 'postal_code', 'city', 'county']
