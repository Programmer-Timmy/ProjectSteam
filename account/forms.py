# edit account form

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from AuthManager.models import CustomUser

class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    public_profile = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    show_friends = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


    class Meta:
        model = CustomUser
        fields = ('username', 'profile_picture', 'public_profile', 'show_friends')

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
            if profile_picture.size > 2 * 1024 * 1024:
                raise ValidationError("Profile picture is too large. Max size is 2MB.")
            else:
                cleaned_data['profile_picture'] = profile_picture

                # Only delete the old picture if a new one is uploaded
                if self.instance.profile_picture and self.instance.profile_picture != profile_picture:
                    self.instance.profile_picture.delete()

        return cleaned_data
