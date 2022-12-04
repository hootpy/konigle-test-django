from datetime import datetime

from celery import shared_task
from customer.models import EmailSubscription


@shared_task
def log_new_subscription():
    current_month = datetime.now().month
    new_subscriptions = EmailSubscription.objects.filter(
        subscribed_at__month=current_month,
        is_subscribed=True,
    ).count()
    print(f"New subscriptions for {current_month}: {new_subscriptions}")
