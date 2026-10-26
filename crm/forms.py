from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'company', 'email', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 5})}
