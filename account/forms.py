# edit account form
import os

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from AuthManager.models import CustomUser

class ProfileEditForm(forms.ModelForm):
    """
    Form for editing the user's profile

    Fields:
    - username: The user's username
    - profile_picture: The user's profile picture
    - public_profile: Whether the user's profile is public
    - show_friends: Whether the user's friends are shown
    - use_steam_profile: Whether the user's Steam profile is used

    Methods:
    - save: Save the form data to the user model
    - clean: Validate the form data
    """
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    public_profile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    show_friends = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    use_steam_profile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'profile_picture', 'public_profile', 'show_friends', 'use_steam_profile')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        profile_picture = cleaned_data.get('profile_picture')

        if username:
            user = CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).first()
            if user:
                raise ValidationError("Username already exists.")
        else:
            raise ValidationError("Username is required.")

        if profile_picture:
            # Validate file size (max size 2MB)

            if os.path.exists(self.instance.profile_picture.path):

                if profile_picture.size > 2 * 1024 * 1024:
                    raise ValidationError("Profile picture is too large. Max size is 2MB.")

                # Only delete the old picture if a new one is uploaded
                if self.instance.profile_picture:
                    self.instance.profile_picture.delete()

                # Set the cleaned_data for the profile picture
                self.cleaned_data['profile_picture'] = profile_picture
            else:
                self.cleaned_data['profile_picture'] = None

        return self.cleaned_data

class UserSettingsForm(forms.ModelForm):
    """
    Form for editing the user's settings

    Fields:
    - opt_out: Whether the user has opted out
    - first_name: The user's first name
    - last_name: The user's last name
    - email: The user's email
    - username: The user's username
    - steam_opt_out: Whether the user has opted out of Steam tracking
    - use_steam_profile: Whether the user's Steam profile is used

    Methods:
    - save: Save the form data to the user model
    """
    opt_out = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    steam_opt_out = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    use_steam_profile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    class Meta:
        model = CustomUser
        fields = ('opt_out', 'first_name', 'last_name', 'email', 'username', 'steam_opt_out', 'use_steam_profile')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class UserChangePasswordForm(forms.ModelForm):
    """
    Form for changing the user's password

    Fields:
    - old_password: The user's old password
    - new_password: The user's new password
    - confirm_password: The user's new password confirmation

    Methods:
    - clean: Validate the form data
    - save: Save the new password to the user model
    """
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')


        user = self.instance
        # Check if the old password is correct
        if old_password and not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")

        # Check if new password matches the confirmation
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("New password and confirmation do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash and set the new password
        user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
        return user
