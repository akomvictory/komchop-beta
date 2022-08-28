# utils file will help us in creating helper functions that we can use throughout the application

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard' # vendor admin page
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard' # customer admin page
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin' # super admin page
        return redirectUrl        