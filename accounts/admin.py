from django.contrib import admin
from .models import User, UserProfile # import user, UserProfile model from current directory
from django.contrib.auth.admin import UserAdmin # import the user admin

# Register your models here.

class CustomUserAdmin(UserAdmin): # this class set the fields to display in the admin panel and also set the password field as non editable
    list_display = ('password', 'email', 'first_name', 'last_name', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
