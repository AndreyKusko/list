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


# class PointSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Point
#         fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        # fields = ('id', 'title', 'parent_point')
        fields = '__all__'

    def get_fields(self):
        fields = super(PointSerializer, self).get_fields()
        fields['sub_points'] = PointSerializer(many=True)
        return fields

# class SubPointSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Point
#         fields = ('name', 'description')
#
#
# class PointSerializer(serializers.ModelSerializer):
#     parent_point = serializers.PrimaryKeyRelatedField()
#     sub_points = serializers.SubPointSerializer()
#
#     class Meta:
#         model = Point
#         fields = (
#             'note',
#             'ordering_number',
#             'title',
#             'parent_point'
#             'text'
#             'is_active'
#             'is_crossed'
#             'updated'
#             'timestamp'
#         )


# class PointSerializer(serializers.ModelSerializer):
#     parent_point = serializers.PrimaryKeyRelatedField()
#
#     class Meta:
#         model = Point
#         fields = (
#             'note',
#             'ordering_number',
#             'title',
#             'parent_point'
#             'text'
#             'is_active'
#             'is_crossed'
#             'updated'
#             'timestamp'
#         )
#
#         def get_related_field(self, model_field):
#             # Handles initializing the `subcategories` field
#             return PointSerializer()
#
#
# PointSerializer.base_fields['subpoints'] = PointSerializer()
