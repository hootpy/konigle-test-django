from customer.models import EmailSubscription
from django.utils import timezone
from rest_framework import serializers


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
                "store": store,
            },
        )
        if not created and not instance.is_subscribed:
            instance.is_subscribed = True
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
            instance.save()
        return instance
