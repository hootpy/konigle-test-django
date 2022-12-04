from customer.models import StoreAPIKey
from rest_framework_api_key.permissions import BaseHasAPIKey


class HasStoreAPIKey(BaseHasAPIKey):
    model = StoreAPIKey
