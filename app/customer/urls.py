from django.urls import path

from customer.views import SubscribeEmailView

urlpatterns = [
    path("subscribe/", SubscribeEmailView.as_view(), name="subscribe"),
]