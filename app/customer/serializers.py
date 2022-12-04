from django.utils import timezone
from rest_framework import serializers

from customer.models import EmailSubscription


class SubscribeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ("email",)

    def save(self, **kwargs):
        store = kwargs.pop("store")
        instance, created = EmailSubscription.objects.get_or_create(
            email=self.validated_data["email"],
            store=store,
            defaults={
                "is_subscribed": True,
                "subscribed_at": timezone.now(),
                "store": store,
            }
        )
        if not created and not instance.is_subscribed:
            instance.is_subscribed = True
            instance.subscribed_at = timezone.now()
            instance.unsubscribe_at = None
            instance.save()
        return instance


class UnsubscribeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ("email",)

    def save(self, **kwargs):
        instance = self.instance
        if instance.is_subscribed:
            instance.is_subscribed = False
            instance.unsubscribe_at = timezone.now()
            instance.save()
        return instance
