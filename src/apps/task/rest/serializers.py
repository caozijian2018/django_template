# -*- coding: utf-8 -*-
from rest_framework import serializers

from apps.task.country import Country
from apps.task.models import App


class AppCreateSerializer(serializers.ModelSerializer):
    files = serializers.FileField()

    class Meta:
        model = App
        exclude = ('create_time', 'update_time', 'package', 'resc_path', 'package_backup_path')


class AppEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        exclude = ('create_time', 'update_time', 'package', 'resc_path', 'package_backup_path')


class AppListSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()

    def get_country_name(self, app):
        return app.country.name

    class Meta:
        model = App
        fields = '__all__'




class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
