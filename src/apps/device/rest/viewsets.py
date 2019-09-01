import json
from datetime import datetime
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.device.models import Slave, Phone
from apps.device.rest.serializers import SlaveHeartbeatSerializer, SlaveSerializer, PhoneHeartbeatSerializer, \
    PhoneListSerializer, SlaveListSerializer, PhoneUpdateSerializer
from apps.utils.utils import CustomPageNumberPagination
import logging

logger = logging.getLogger('__name__')


class SlaveViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Slave.objects.all().order_by('-create_time')
    permission_classes = ()
    authentication_classes = ()
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return SlaveHeartbeatSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return SlaveSerializer
        return SlaveListSerializer

    def create(self, request, *args, **kwargs):
        mac = request.data['mac']
        instance = self.get_object(mac)
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
            instance.last_heartbeat = datetime.now()
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self, mac):
        try:
            return Slave.objects.get(mac=mac)
        except Exception as e:
            pass
        return None

    def update(self, request, *args, **kwargs):
        mac = request.data['mac']
        instance = self.get_object(mac)
        if not instance:
            logger.error("unknow slave {}!".format(mac))
            raise serializers.ValidationError("unknow slave!")
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class PhoneViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Phone.objects.get_queryset().order_by('pk')
    permission_classes = ()
    authentication_classes = ()
    serializer_class = PhoneUpdateSerializer
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return PhoneHeartbeatSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return PhoneUpdateSerializer
        return PhoneListSerializer

    def get_slave(self, mac):
        try:
            return Slave.objects.get(mac=mac)
        except Exception as e:
            pass
        return None

    def create(self, request, *args, **kwargs):
        data = request.data
        phones = data['phones']
        server_mac = data['server_mac']
        slave = self.get_slave(mac=server_mac)
        if not slave:
            return Response(request.data, status=status.HTTP_201_CREATED)
        for phone in phones:
            phone_uuid = phone.get('uuid', None)
            phone_status = phone.get('status', Phone.PHONE_ONLINE)
            instance = self.get_instance(uuid=phone_uuid)

            if instance is None:
                instance = Phone()
                instance.uuid = phone_uuid
            else:
                instance.last_heartbeat = datetime.now()
            instance.status = phone_status
            instance.slave = slave
            instance.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        uuid = request.data['uuid']
        instance = self.get_instance(uuid)
        if not instance:
            logger.error("unknow Phone {}!".format(uuid))
            raise serializers.ValidationError("unknow Phone!")
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_instance(self, uuid):
        if uuid:
            try:
                return Phone.objects.get(uuid=uuid)
            except Exception as e:
                pass
        return None
