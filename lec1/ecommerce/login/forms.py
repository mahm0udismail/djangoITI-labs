from django import forms

from .models import LoginAttempt

class LoginForm(forms.Form):
    class Meta:
        model = LoginAttempt
        '__all__'