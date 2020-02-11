# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app1_accounts import models as app1_models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data.get("username")
        email = data.get("username").lower()
        if User.objects.filter(email=username).exists():
            raise ValueError("Email %s is already registered" % email)
        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['username'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data["password"]
        if not username:
            raise ValueError("A username required to login.")
        user = User.objects.filter(username=username).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()

        else:
            raise ValueError("The username or email is not valid.")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValueError("Something is incorrect.")
        data["token"] = "RANDOM TOKEN"
        return data


class LibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = app1_models.Library
        fields = '__all__'
