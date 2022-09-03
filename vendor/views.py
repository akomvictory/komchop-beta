from django.shortcuts import get_object_or_404, render

from accounts.models import UserProfile
from .forms import VendorForm
from accounts.forms import UserProfileForm
from .models import Vendor

def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user) #we get userprofile data of the logged in user
    vendor = get_object_or_404(Vendor, user=request.user) #we get vendor data of the logged in user

    profile_form = UserProfileForm(instance= profile) #by passing this instance we can load data from userprofile model into the form
    vendor_form = VendorForm(instance= vendor) #by passing this instance we can load data from vendor model into the form

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile
    }
    return render(request, 'vendor/vprofile.html', context)
