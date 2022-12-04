from datetime import datetime

from celery import shared_task
from customer.models import EmailSubscription


@shared_task
def log_new_subscription():
    current_month = datetime.now().month
    current_year = datetime.now().year
    new_subscriptions = EmailSubscription.objects.filter(
        last_updated__month=current_month,
        last_updated__year=current_year,
        is_subscribed=True,
    ).count()
    print(f"New subscriptions for {current_month}: {new_subscriptions}")
