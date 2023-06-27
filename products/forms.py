from django import forms
from .models import Products, Bidding

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'location', 'image', 'category', 'base_price', 'deadline', 'shipping_charges', 'returns', 'description', 'specifications']
