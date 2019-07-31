# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class NotebookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notebook
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'
    #
    sub_points = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_points")

    def get_child_points(self, obj):
        """ self referral field """
        serializer = PointSerializer(
            instance=obj.sub_points.filter(is_deleted=False),
            many=True
        )
        return serializer.data




