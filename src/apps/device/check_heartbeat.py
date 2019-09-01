# _*_ encoding: utf-8 _*_

import logging
from datetime import datetime

from django.conf import settings
from apps.device.models import Phone, Slave

logger = logging.getLogger('__name__')


def check_phone():
    now = datetime.now()
    phones = Phone.objects.filter(status=Phone.PHONE_ONLINE)
    for phone in phones:
        if (now - phone.last_heartbeat).seconds > settings.PHONE_HEARTBEAT_TIMEOUT:
            phone.status = Phone.PHONE_OFFLINE
            phone.save()
            logger.info("check phone heartbeat failed--{0}--{1}".format(phone.uuid, phone.last_heartbeat))


def check_slave():
    now = datetime.now()
    slaves = Slave.objects.filter(status=Slave.SLAVE_ONLINE)
    for slave in slaves:
        if (now - slave.last_heartbeat).seconds > settings.SLAVE_HEARTBEAT_TIMEOUT:
            slave.status = Slave.SLAVE_OFFLINE
            slave.save()
            logger.info("check slave heartbeat failed--{0}--{1}".format(slave.mac, slave.ip, slave.last_heartbeat))
