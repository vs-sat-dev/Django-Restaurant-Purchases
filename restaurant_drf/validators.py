from rest_framework.serializers import ValidationError


class LessThanValidator:
    def __init__(self, base, field_name='Field', is_char=True):
        self.base = base
        self.is_char = is_char
        self.field_name = field_name
    
    def __call__(self, value):
        if self.is_char:
            if len(value) < self.base:
                raise ValidationError({'error': f'{self.field_name} must be greater or equal than {self.base} symbols'})
        else:
            if value < self.base:
                raise ValidationError({'error': f'{self.field_name} must be greater or equal than {self.base}'})


class GreaterThanValidator:
    def __init__(self, base, field_name='Field', is_char=True):
        self.base = base
        self.is_char = is_char
        self.field_name = field_name
    
    def __call__(self, value):
        if self.is_char:
            if len(value) > self.base:
                raise ValidationError({'error': f'{self.field_name} must be less or equal than {self.base} symbols'})
        else:
            if value > self.base:
                raise ValidationError({'error': f'{self.field_name} must be less or equal than {self.base}'})

