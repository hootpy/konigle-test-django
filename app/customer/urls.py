from customer.views import SubscribeEmailView, UnsubscribeEmailView
from django.urls import path

urlpatterns = [
    path("subscribe/", SubscribeEmailView.as_view(), name="subscribe"),
    path("unsubscribe/", UnsubscribeEmailView.as_view(), name="unsubscribe"),
]
