import logging
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("konigle")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    "log_new_subscription": {
        "task": "customer.tasks.log_new_subscription",
        "schedule": crontab(day_of_week="mon,wed", hour=12, minute=12),
    },
}

logger = logging.getLogger(__name__)
