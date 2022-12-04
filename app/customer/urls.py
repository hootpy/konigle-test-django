from django.urls import path

from customer.views import SubscribeEmailView, UnsubscribeEmailView

urlpatterns = [
    path("subscribe/", SubscribeEmailView.as_view(), name="subscribe"),
    path("unsubscribe/", UnsubscribeEmailView.as_view(), name="unsubscribe"),
]