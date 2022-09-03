from dataclasses import field
from django.core.exceptions import ValidationError # we import ValidationError
from django import forms # we import django form library to bind with our html fields
from .models import User, UserProfile

# The django forms feature enable us create html form out of our models fields
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']


    def clean(self): #this function is for handling field error to ensure password matches confirm_password
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'})) #we difine the css styling for the profile pic input field
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'})) #we difine the css styling for the cover photo pic input field
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']
