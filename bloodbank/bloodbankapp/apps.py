from django.apps import AppConfig


class DemoappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bloodbankapp"

INSTALLED_APPS = [

    'crispy_forms',
]
