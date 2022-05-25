from django import forms

from .models import Ingridient


class IngridientForm(forms.ModelForm):
    name = forms.CharField(max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    quantity = forms.FloatField()
    unit = forms.CharField(max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit'}))
    unit_price = forms.FloatField()

    class Meta:
        model = Ingridient
        fields = ['__all__']
