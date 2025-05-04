from django.apps import AppConfig


class DemoappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bloodbankapp"


class BloodbankappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodbankapp'

    def ready(self):
        # Import signals when app is ready
        import bloodbankapp.signals

INSTALLED_APPS = [

    'crispy_forms',
]
