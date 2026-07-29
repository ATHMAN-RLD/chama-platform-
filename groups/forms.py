from django import forms
from .models import Chama
from .models import Repayment

class ChamaForm(forms.ModelForm):
    class Meta:
        model = Chama
        fields = ['name', 'description', 'contribution_amount', 'contribution_frequency']  

class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ['amount', 'payment_method', 'transaction_reference']  