from rest_framework import serializers

from restaurant.models import Ingridient, MenuItem, RecipeRequirement, Purchase
from .validators import LessThanValidator, GreaterThanValidator


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[LessThanValidator(1, field_name='Name'), 
                                             GreaterThanValidator(64, field_name='Name')])
    quantity = serializers.FloatField(validators=[LessThanValidator(0, field_name='Quantity', is_char=False), 
                                                  GreaterThanValidator(1000000, field_name='Quantity', is_char=False)])
    unit = serializers.CharField(validators=[LessThanValidator(1, field_name='Unit'), 
                                             GreaterThanValidator(64, field_name='Unit')])
    unit_price = serializers.FloatField(validators=[LessThanValidator(0, field_name='Unit Price', is_char=False), 
                                                  GreaterThanValidator(1000000, field_name='Unit Price', is_char=False)])
    
    class Meta:
        model = Ingridient
        fields = ['name', 'quantity', 'unit', 'unit_price']


