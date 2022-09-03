from email import message
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import UserProfile
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import Vendor
from django.contrib import messages

def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user) #we get userprofile data of the logged in user
    vendor = get_object_or_404(Vendor, user=request.user) #we get vendor data of the logged in user

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile) #here we get the post data with file data associated with instance of logged in user
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor) #here we get the post data with file data associated with instance of logged in user

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated')
            return redirect('vprofile')

        else:
            print(profile_form.errors)   
            print(vendor_form.errors)  

    else:
        profile_form = UserProfileForm(instance= profile) #by passing this instance we can load data from userprofile model into the form
        vendor_form = VendorForm(instance= vendor) #by passing this instance we can load data from vendor model into the form

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile
    }
    return render(request, 'vendor/vprofile.html', context)
