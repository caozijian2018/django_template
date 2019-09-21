# -*- coding: utf-8 -*-
from rest_framework import serializers

from apps.task.country import Country
from apps.task.models import Imgs, News


class AppListSerializer(serializers.ModelSerializer):
    # country_name = serializers.SerializerMethodField()

    # def get_country_name(self, app):
    #     return app.country.name

    class Meta:
        model = Imgs
        fields = '__all__'




class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ("create_time", "update_time")


class ImgsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imgs
        fields = "__all__"

class ImgsCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imgs
        fields = ('name', )