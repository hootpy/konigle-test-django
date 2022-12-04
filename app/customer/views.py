from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import SubscribeEmailSerializer


class SubscribeEmailView(GenericAPIView):
    serializer_class = SubscribeEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"success": True}, status=status.HTTP_201_CREATED)

class UnsubscribeEmailView(GenericAPIView):
    serializer_class = SubscribeEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"success": True}, status=status.HTTP_201_CREATED)