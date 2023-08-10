from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None

        if user.is_staff and not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_staff'].disabled = True
            self.fields['is_superuser'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'special_user', 'is_staff', 'is_superuser']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

