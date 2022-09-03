from django import forms # we import django form library to bind with our html fields
from .models import Vendor

# The django forms feature enable us create html form out of our models fields
class VendorForm(forms.ModelForm):
    vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'})) #we difine the css styling for the profile pic input field
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']