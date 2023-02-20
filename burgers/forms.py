from django import forms
from .models import Burger, BurgerOrder

class BurgerOrderForm(forms.ModelForm):
    burger = forms.ModelChoiceField(queryset=Burger.objects.distinct())
    toppings = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    quantity = forms.IntegerField(min_value=1, max_value=10, initial=1)
    class Meta:
        model = BurgerOrder
        fields = ['burger', 'toppings', 'quantity']