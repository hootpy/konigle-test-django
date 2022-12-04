from django.core.management import BaseCommand

from customer.models import Store, StoreAPIKey


class Command(BaseCommand):

    def handle(self, *args, **options):
        store_name = input('Store name: ')
        store, created = Store.objects.get_or_create(name=store_name)
        api_key, key = StoreAPIKey.objects.create_key(store=store, name=f"{store_name} API Key")
        self.stdout.write(self.style.SUCCESS(f'Successfully created API key for store: {key}'))
