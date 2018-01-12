# app.py specifies custom application configuration for the application.
# To illustrate, since signals.py is an independently defined file, we need to load this manually.
# For more see https://docs.djangoproject.com/en/dev/ref/applications/#application-configuration

from django.apps import AppConfig


# Defines a new class for the application configuration (name just refers to what the configuration does).
class StaticContainersConfig(AppConfig):
    name = 'static_containers'

    def ready(self):
        import static_containers.signals
