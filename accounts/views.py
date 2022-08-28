from django.shortcuts import render, redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages # we import messages library to give feedback when new user is created

# Create your views here.

def registerUser(request):
    if request.method == 'POST': # we check the request type from user
        form = UserForm(request.POST) #we use the the request body as our form data
        if form.is_valid():
            password = form.cleaned_data['password'] #here we clean password value from user
            user = form.save(commit=False) # here the form is ready to be save but not yet and we can assign values to the user object created
            user.set_password(password) # here we hash the user provided password
            user.role = User.CUSTOMER # here we use the user object we created to assigned newly registered user as customer defaultly
            user.save() # here we save the user registerUser
            messages.success(request, 'User account has been created successfully') # give output when user is successfully created
            return redirect('registerUser')       # this will execute if request type from user is POST
        else: # this will executed if user data  does not validate true
            print(form.errors)   
    else:                           # this will execute if request type from user is GET
        form = UserForm() #we use the User model form to make fields for the HTML register template
    
    context = { #the context dictionary is set on GET or POST request
        'form': form,
    }

    return render(request, 'accounts/registerUser.html', context)
    
def registerVendor(request):
    if request.method == 'POST':
        #store the data and create the user
        form = UserForm(request.POST) # here we get post data from the user form
        v_form = VendorForm(request.POST, request.FILES) # here we get post data from the vendor form, with vendor license using (request.FILES)
        if form.is_valid() and v_form.is_valid(): # here we check if data from user, vendor form are valid
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False) # here the form is ready to be save but not yet and we can assign values to the vendor object created
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user) # this will bring user profile for the user
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'User account has been created successfully! Please wait for approval') # give output when user is successfully created
            return redirect('registerVendor')
        else:
            print(form.errors) #here we display errors if form data is not valid 
    else:
        form = UserForm() # here we get the user form without post data (get method)
        v_form = VendorForm() # here we get the vendor form without post data (get method)

    context = { # here we pass form fields to html template
        'form': form,
        'v_form': v_form
    }
    return render(request, 'accounts/registerVendor.html', context)    
