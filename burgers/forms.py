from django import forms
from .models import Burger, BurgerOrder



class BurgerOrderForm(forms.ModelForm):
    burger = forms.ModelMultipleChoiceField(
        queryset=Burger.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = BurgerOrder
        fields = ['customer_name', 'burger']