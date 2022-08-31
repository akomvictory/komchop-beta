from base64 import urlsafe_b64decode
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied #permission library to restrict access

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import auth, messages # we import messages library to give feedback when new user is created
#we import auth library to authenticate user

from .utils import detectUser, send_verification_email #import functions from utils file
from django.contrib.auth.decorators import login_required, user_passes_test #decorator accessible to only logged in users and users that passes test on certain criteria

#Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True 
    else:
        raise PermissionDenied


#Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True 
    else:
        raise PermissionDenied


# Create your views here.

def registerUser(request):
    if request.user.is_authenticated: #check if user is already logged in
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST': # we check the request type from user
        form = UserForm(request.POST) #we use the the request body as our form data
        if form.is_valid():
            password = form.cleaned_data['password'] #here we clean password value from user
            user = form.save(commit=False) # here the form is ready to be save but not yet and we can assign values to the user object created
            user.set_password(password) # here we hash the user provided password
            user.role = User.CUSTOMER # here we use the user object we created to assigned newly registered user as customer defaultly
            user.save() # here we save the user registerUser

            #send verification email
            send_verification_email(request, user)

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
    if request.user.is_authenticated: #check if user is already logged in
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
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
            send_verification_email(request, user) # sent email verification to user

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


def activate(request, uidb64, token):
    #activate the user by setting the is_active status to True
    try:
        uid = urlsafe_b64decode(uidb64).decode() #we get user uidcode via get method
        user = User._default_manager.get(pk=uid) # get the user we want to activate
    except(TypeError, ValueError, OverflowError, User.DoesNotExist): # if we get any error regarding the user 
        User = None # we set user as not found
    if user is not None and default_token_generator.check_token(user, token): # we validate the user token
        user.is_active = True # set user active state to true
        user.save()
        messages.success(request, "Congratulation your account is activated")
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('myAccount')




def login(request):
    if request.user.is_authenticated: #check if user is already logged in
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST': #here we check if it a post request and user is not yet logged in
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password) # here we authenticate the user with provided email & password

        if user is not None: # this will check that login fields are registered
            auth.login(request, user) # here we log in the user
            messages.success(request, 'You are now logged in') # give output when user is successfully logged in
            return redirect('myAccount') #we redirect user to the dashboard page

        else: # executes when login details are incorrect
            messages.error(request, 'Invalid login credentials') # give output when user provides invalid login details
        return redirect('login') #we redirect user back to the login page

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

@login_required(login_url='login') #only logged in users can access this view
def myAccount(request):
    user = request.user # gets current logged in user
    redirectUrl = detectUser(user) # detects page to redirect logged in user to
    return redirect(redirectUrl)

@login_required(login_url='login') #only logged in users can access this view
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login') #only logged in users can access this view
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')    


