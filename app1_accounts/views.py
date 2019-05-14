
from django.shortcuts import render, get_object_or_404
import jwt,json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import LibrarySerializer, UserSerializer
from .models import *
from django.http import HttpResponse

from django.contrib.auth import get_user_model
User = get_user_model()


class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            get_token(user)
            # user_token = Token.objects.create(user=user)
            data = {'token': get_token(user)}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def get_token(user):
    try:
        user_token = user.auth_token.key
    except:
        user_token = Token.objects.create(user=user)
    return user_token


from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class LibraryApiView(APIView):
    model = Library
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    serializer_class = LibrarySerializer

    def get(self, request):
        queryset = self.model.objects.get_or_create(user=request.user)
        id_value = request.query_params.get('id', None)
        if id_value:
            queryset = get_object_or_404(self.model, id=id_value)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

        # return queryset

    # def put(self, request):
    #     print('> create')
    #     notebooks_qty = self.model.objects.filter(library_id=request.data.library_id).count()
    #     user = User.objects.get(id=1)
    #     queryset = self.model.objects.create(user=user,
    #                                          title=notebooks_qty+1,
    #                                          ordering_number=notebooks_qty+1)
    #     return queryset
    #
    # def update(self, request):
    #     print('> update')
    #     queryset = self.model.objects.get(id=request)
    #     title = request.data.get('title', None)
    #     if title:
    #         queryset.title = title
    #     queryset.save()
    #     return queryset
    #
    # def delete(self, request):
    #     print('> delete')
    #     queryset = self.model.delete(id=request.query_params['id'])
    #     return queryset