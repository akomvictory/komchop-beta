from email import message
from email.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site # library to get the current site domain
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
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

#send verification email
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL # we we set how the email subject send to user should look like
    current_site = get_current_site(request) # get the current site domain
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user), #we make token that we pass to the user
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()

def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()