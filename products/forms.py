from django import forms
from .models import Product, InventoryProduct, RateProduct
from django.core.validators import MinValueValidator, MaxValueValidator


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'label',
            'description',
            'price',
            'image',
            'image_url',
            'category_id',
        ]


class InventoryProductForm(forms.ModelForm):
    class Meta:
        model = InventoryProduct
        fields = ['id_size', 'quantity']

    def __init__(self, *args, **kwargs):
        super(InventoryProductForm, self).__init__(*args, **kwargs)
        self.fields['id_size'].required = False


class RateProductForm(forms.ModelForm):
    rate = forms.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        model = RateProduct
        fields = ['rate']
