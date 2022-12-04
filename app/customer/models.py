from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)


class StoreAPIKey(AbstractAPIKey):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="api_keys")


class EmailSubscription(models.Model):
    email = models.EmailField(max_length=254)
    is_subscribed = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="email_subscriptions",
        null=True,
    )

    def __str__(self):
        return self.email

    class Meta:
        unique_together = ("email", "store")

    status = property(lambda self: "Subscribed" if self.is_subscribed else "Unsubscribed")

    @property
    def timestamp(self):
        tz_utc = pytz.timezone("UTC")
        return self.convert_time_to_text_from_second(datetime.now(tz=tz_utc) - self.last_updated)

    @staticmethod
    def convert_time_to_text_from_second(datetime_delta):
        days = datetime_delta.days
        hours = datetime_delta.seconds // 3600
        minutes = (datetime_delta.seconds // 60) % 60
        seconds = datetime_delta.seconds % 60
        if days > 0:
            return f"{days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return f"{seconds} seconds ago"
