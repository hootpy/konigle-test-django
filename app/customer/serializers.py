from django.utils import timezone
from rest_framework import serializers

from customer.models import EmailSubscription


class SubscribeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ("email",)

class UnsubscribeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ("email",)

    def save(self, **kwargs):
        instance = EmailSubscription.objects.get(email=self.validated_data["email"])
        instance.unsubscribe_at = timezone.now()
        instance.save()
        return instance