from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and password.

    Attributes:
    - first_name: The user's first name.
    - last_name: The user's last name.
    - email: The user's email address.
    - username: The user's username.
    - opt_out: A boolean field to opt out of emails.
    - password1: The user's password.
    - password2: The user's password confirmation.

    Methods:
    - save: Save the user to the database.
    """
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    opt_out = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'opt_out')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    """
    A form that authenticates a user based on the given username and password.

    Attributes:
    - username: The user's username.
    - password: The user's password.

    Methods:
    - clean: Validate the username and

    password and authenticate the user.
    """
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            if not CustomUser.objects.filter(username=username).exists():
                raise ValidationError("Invalid username or password.")

            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError("Invalid username or password.")


        return cleaned_data



