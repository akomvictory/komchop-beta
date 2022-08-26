from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self): #this is the function that will make the signals work in the signal.py file work
        import accounts.signals
