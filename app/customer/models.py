from django.contrib.auth.models import User
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)

class StoreAPIKey(AbstractAPIKey):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="api_keys")


class EmailSubscription(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    is_subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(null=True, blank=True)
    unsubscribe_at = models.DateTimeField(null=True, blank=True)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="email_subscriptions",
        null=True,
    )


    def __str__(self):
        return self.email