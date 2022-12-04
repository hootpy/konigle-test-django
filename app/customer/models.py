from django.db import models

# Create your models here.
class EmailSubscription(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_at = models.DateTimeField(null=True, blank=True)



    is_subscribed = property(lambda self: self.unsubscribe_at is None)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.unsubscribe_at is not None:
            self.email = f"{self.email.split('@')[0]}+{self.unsubscribe_at.timestamp()}@{self.email.split('@')[1]}"
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Email Subscriptions"
        verbose_name = "Email Subscription"
        db_table = "email_subscription"