from django import forms
from . import models

class Update(forms.ModelForm):
    class Meta:
        model = models.SexToys
        fields = ['title', 'about']

