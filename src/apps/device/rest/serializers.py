# -*- coding: utf-8 -*-
from rest_framework import serializers
from apps.device.models import Slave, Phone


class SlaveHeartbeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slave
        fields = ('mac', 'ip')


class SlaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slave
        fields = ('mac', 'ip', 'status')


class SlaveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slave
        fields = '__all__'


class PhoneHeartbeatSerializer(serializers.ModelSerializer):
    phones = serializers.JSONField()
    server_mac = serializers.SerializerMethodField()
    server_ip = serializers.SerializerMethodField()

    def get_server_mac(self, PhoneHeart):
        try:
            return Slave.objects.get(mac=PhoneHeart.server_mac)
        except Exception as e:
            print(e)
            pass
        return None

    class Meta:
        model = Phone
        fields = ('phones', 'server_mac', 'server_ip')


class PhoneUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('country', 'platform', 'uuid', 'tag', 'slave', 'is_idle', 'can_recharge', 'is_stop')


class PhoneListSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()

    def get_country_name(self, phone):
        return phone.country.name if phone.country else None

    class Meta:
        model = Phone
        fields = '__all__'
