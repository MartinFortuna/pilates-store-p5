from django import forms
from .models import Order
from profiles.forms import UserForm, UserProfileForm


class CheckoutForm(forms.ModelForm):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': 'readonly'}))
    first_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    last_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    telephone = forms.CharField(max_length=25)
    address1 = forms.CharField(max_length=50)
    address2 = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=25)
    county = forms.CharField(max_length=25)

    class Meta:
        model = Order
        fields = ['username', 'email', 'first_name', 'last_name', 'telephone', 'address1', 'address2', 'postal_code', 'city', 'county']