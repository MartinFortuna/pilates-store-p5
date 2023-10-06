from django import forms
from .models import RateProduct
from django.core.validators import MinValueValidator, MaxValueValidator


class RateProductForm(forms.ModelForm):
    rate = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        model = RateProduct
        fields = ['rate']
