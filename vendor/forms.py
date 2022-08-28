from django import forms # we import django form library to bind with our html fields
from .models import Vendor

# The django forms feature enable us create html form out of our models fields
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']