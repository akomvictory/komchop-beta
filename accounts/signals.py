from django.db.models.signals import post_save, pre_save # here we import the post save signal
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs): 
    print(created)
    if created: # this will execute once a user has been created and will initiate creating a profile for that user
        UserProfile.objects.create(user=instance) # create userprofile when a user is created
    else:
        try:
            profile = UserProfile.objects.get(user=instance) # update userprofile when a user is updated
            profile.save()
        except:
            # create the userprofile if not exist
            UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass

# post_save.connect(post_save_create_profile_receiver, sender=User)
        