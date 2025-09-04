from django import forms

class CalculationForm(forms.Form):
    number1 = forms.FloatField(label="Number 1")
    number2 = forms.FloatField(label="Number 2")
    number3 = forms.FloatField(label="Number 3")

    OP_CHOICES = [
        ('+', 'Add (+)'),
        ('-', 'Subtract (-)'),
        ('*', 'Multiply (×)'),
        ('/', 'Divide (÷)'),
    ]
    operator = forms.ChoiceField(choices=OP_CHOICES, label="Operator")

    def clean(self):
        cleaned = super().clean()
        op = cleaned.get('operator')
        n2 = cleaned.get('number2')
        n3 = cleaned.get('number3')

        # Basic safety: if dividing, prevent division by zero in any step we might do.
        if op == '/' and ((n2 is not None and n2 == 0) or (n3 is not None and n3 == 0)):
            raise forms.ValidationError("Division by zero is not allowed.")
        return cleaned
