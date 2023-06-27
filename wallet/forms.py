from django import forms

class AddFundsForm(forms.Form):
    amount = forms.FloatField(label='Amount')
