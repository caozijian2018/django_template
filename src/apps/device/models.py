from django.db import models
from django.forms import model_to_dict

from apps.task.country import Country


class Slave(models.Model):
    SLAVE_ONLINE = 0
    SLAVE_OFFLINE = 1
    SLAVE_STATUS = (
        (SLAVE_ONLINE, 'online'),
        (SLAVE_OFFLINE, 'offline')
    )

    mac = models.CharField(max_length=100, verbose_name="设备ID", help_text="设备ID", unique=True)
    ip = models.CharField(max_length=20, verbose_name="ip", help_text="ip")
    status = models.IntegerField(default=SLAVE_ONLINE, choices=SLAVE_STATUS, verbose_name='主机状态',
                                 help_text='主机状态 0 在线 ,1 离线')
    last_heartbeat = models.DateTimeField(auto_now_add=True, verbose_name='上次心跳的时间戳')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建主机时间", help_text='创建主机时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改主机时间", help_text='修改主机时间')

    class Meta:
        verbose_name = u'Slave'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

    def to_dict(self):
        item = model_to_dict(self)
        return item


class Phone(models.Model):
    PHONE_ANDROID = 0
    PHONE_IOS = 1
    PHONE_PLATFORM = {
        (PHONE_ANDROID, 'Android'),
        (PHONE_IOS, 'IOS')
    }
    PHONE_ONLINE = 0
    PHONE_OFFLINE = 1
    PHONE_DISABLED = 2
    PHONE_STATUS = {
        (PHONE_ONLINE, 'online'),
        (PHONE_OFFLINE, 'offline'),
        (PHONE_DISABLED, 'disabled')
    }
    country = models.ForeignKey(Country, verbose_name="国家", help_text="国家", blank=True, null=True)
    platform = models.IntegerField(default=1, choices=PHONE_PLATFORM, verbose_name='手机类型 0 ANDROID， 1 IOS',
                                   help_text='手机类型 0 ANDROID， 1 IOS')
    uuid = models.CharField(max_length=100, verbose_name="设备ID", help_text="设备ID", unique=True)
    tag = models.CharField(max_length=30, null=True, blank=True, verbose_name="编号", help_text="编号")
    status = models.IntegerField(default=PHONE_ONLINE, choices=PHONE_STATUS, verbose_name='手机状态', help_text='手机状态')
    slave = models.ForeignKey(Slave, verbose_name="主机")
    is_idle = models.BooleanField(default=True, verbose_name="是否空闲", help_text="是否空闲 布尔值")
    is_stop = models.BooleanField(default=False, verbose_name="是否暂停", help_text="是否暂停")
    can_recharge = models.BooleanField(default=False, verbose_name="可否充值", help_text="可否充值 布尔值")
    last_heartbeat = models.DateTimeField(auto_now_add=True, verbose_name='上次心跳的时间戳')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建手机时间", help_text='创建手机时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改手机时间", help_text='修改手机时间')

    class Meta:
        verbose_name = u'Phone'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag

    def to_dict(self):
        item = model_to_dict(self)
        return item
