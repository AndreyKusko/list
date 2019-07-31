
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app1_accounts import (
    models as app1_models,
    serializers as app1_serializers,
    utils as app1_utils
)

User = get_user_model()


class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        serializer = app1_serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            data = {'token': app1_utils.get_token(user)}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LibraryApiView(APIView):
    model = app1_models.Library
    permission_classes = [IsAuthenticated]
    serializer_class = app1_serializers.LibrarySerializer

    def get(self, request):
        queryset = self.model.objects.get_or_create(user=request.user)
        id_value = request.query_params.get('id', None)
        if id_value:
            queryset = get_object_or_404(self.model, id=id_value)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
