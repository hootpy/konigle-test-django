from customer.models import EmailSubscription, StoreAPIKey
from customer.permissions import HasStoreAPIKey
from customer.serializers import SubscribeEmailSerializer, UnsubscribeEmailSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
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
