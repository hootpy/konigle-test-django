from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_data():
    pass

class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer'

    def ready(self):
        post_migrate.connect(create_default_data, sender=self)
