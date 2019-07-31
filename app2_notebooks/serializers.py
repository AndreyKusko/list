# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app2_notebooks import models as app2_models

User = get_user_model()


class NotebookSerializer(serializers.ModelSerializer):

    class Meta:
        model = app2_models.Notebook
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = app2_models.Note
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = app2_models.Point
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
