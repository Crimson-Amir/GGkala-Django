from django import forms
from .models import ReviewModel


class ReviewForms(forms.Form):
    comment_title = forms.CharField(max_length=50)
    comment_body = forms.CharField(max_length=500)
