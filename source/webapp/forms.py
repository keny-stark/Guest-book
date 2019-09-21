from django import forms
from django.forms import widgets


class ListForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Name')
    text = forms.CharField(max_length=2000, required=True,  label='Text', widget=widgets.Textarea)
    email = forms.EmailField(label='Email', required=True)
