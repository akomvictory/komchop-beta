from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
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