from django import forms
from .models import Chama

class ChamaForm(forms.ModelForm):
    class Meta:
        model = Chama
        fields = ['name', 'description', 'contribution_amount', 'contribution_frequency']   