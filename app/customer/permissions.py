from rest_framework_api_key.permissions import BaseHasAPIKey
from customer.models import StoreAPIKey

class HasStoreAPIKey(BaseHasAPIKey):
    model = StoreAPIKey
