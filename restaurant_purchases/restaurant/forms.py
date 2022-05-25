from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Ingridient, MenuItem, RecipeRequirement, Purchase


class IngridientForm(forms.ModelForm):
    name = forms.CharField(max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.FloatField(
        validators=[MinValueValidator(0.001), MaxValueValidator(1000000)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
        )
    unit = forms.CharField(max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    unit_price = forms.FloatField(
        validators=[MinValueValidator(0.001), MaxValueValidator(1000000)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
        )

    class Meta:
        model = Ingridient
        fields = ['name', 'quantity', 'unit', 'unit_price']


class MenuItemForm(forms.ModelForm):
    title = forms.CharField(max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(
        validators=[MinValueValidator(0.001), MaxValueValidator(1000000)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
        )

    class Meta:
        model = MenuItem
        fields = ['title', 'price']
