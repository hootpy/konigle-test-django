from datetime import datetime

from customer.models import EmailSubscription, Store, StoreAPIKey
from customer.permissions import HasStoreAPIKey
from customer.serializers import SubscribeEmailSerializer, UnsubscribeEmailSerializer
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class SubscribeEmailView(GenericAPIView):
    serializer_class = SubscribeEmailSerializer
    permission_classes = [HasStoreAPIKey]

    def post(self, request):
        key = request.META["HTTP_X_API_KEY"]
        store = StoreAPIKey.objects.get_from_key(key).store
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"success": False, "message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(store=store)
        return Response(data={"success": True}, status=status.HTTP_200_OK)


class UnsubscribeEmailView(GenericAPIView):
    serializer_class = UnsubscribeEmailSerializer
    permission_classes = [HasStoreAPIKey]

    def post(self, request):
        key = request.META["HTTP_X_API_KEY"]
        store = StoreAPIKey.objects.get_from_key(key).store
        try:
            instance = EmailSubscription.objects.get(email=request.data["email"], store=store)
        except EmailSubscription.DoesNotExist:
            return Response(
                data={"success": False, "message": "Email does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(instance=instance)
        serializer.save()
        return Response(data={"success": True}, status=status.HTTP_200_OK)


class CustomerEmailView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    current_month_text = property(lambda self: datetime.now().strftime("%b"))
    current_month = property(lambda self: datetime.now().month)
    current_year = property(lambda self: datetime.now().year)

    def get(self, request):
        context = {
            "month": self.current_month_text,
            "year": self.current_year,
            "email_list": 0,
            "new_this_month": 0,
            "unsubscribed": 0,
        }
        store_name = request.session.get("store_name", None)
        if not store_name:
            return Response(data={}, template_name="login.html")
        context["store_name"] = store_name
        store, created = Store.objects.get_or_create(name=store_name)
        email_list = EmailSubscription.objects.filter(
            store=store,
            last_updated__month=self.current_month,
            last_updated__year=self.current_year,
        ).order_by("-last_updated")
        context["email_list"] = email_list.count()
        context["new_this_month"] = email_list.filter(is_subscribed=True).count()
        context["unsubscribed"] = email_list.filter(is_subscribed=False).count()
        context["emails"] = email_list
        return Response(data=context, template_name="index.html")

    def post(self, request):
        request.session["store_name"] = request.data["store_name"]
        return HttpResponseRedirect(reverse("email"))


class LogoutView(GenericAPIView):
    def get(self, request):
        request.session.flush()
        return HttpResponseRedirect(reverse("email"))
