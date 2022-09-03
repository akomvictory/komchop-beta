from vendor.models import Vendor
#this script will be available through out the application

def get_vendor(request): 
    try:
       vendor = Vendor.objects.get(user=request.user)  #we can use this throught out the application
    except:
        vendor = None
    return dict(vendor=vendor)