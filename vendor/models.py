from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
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

    def save(self, *args, **kwargs): # this function run when a vendor is created
        if self.pk is not None: 
            #update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved: #check that approval status is not same before sending notification
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                    
                if self.is_approved == True:
                    #send notification email
                    mail_subject = "Congratulations! your restaurant has been approved"
                    send_notification(mail_subject, mail_template, context)
                else:
                    #send notification email   
                    mail_subject = "We're sorry you are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template, context)


        return super(Vendor, self).save(*args, **kwargs)   