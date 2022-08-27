from django.db import models
from accounts.models import User, UserProfile
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE) # user field has one to one relationship in the User model
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE) # user_profile field has one to one relationship in the UserProfile model
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license') #vendor has to provide document image before they can be approved
    is_approved = models.BooleanField(default=False) # approval status is set as unapproved by default
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor_name