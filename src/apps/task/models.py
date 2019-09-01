from django.contrib import admin
from django.db import models
from django.forms import model_to_dict
from jsonfield import JSONField

from apps.device.models import Phone
from apps.task.country import Country


class App(models.Model):
    APP_PLATFORM = {
        (0, 'Android'),
        (1, 'IOS')
    }
    platform = models.IntegerField(default=1, choices=APP_PLATFORM, verbose_name='app类型', help_text='app类型')
    name = models.CharField(max_length=20, verbose_name="App名字", help_text="App名字")
    package = models.CharField(max_length=100, verbose_name="package下载地址", help_text="package下载地址")
    package_name = models.CharField(max_length=100, verbose_name="package名称", help_text="package名称")
    package_backup_path = models.CharField(max_length=100, verbose_name="package备份文件路径", help_text="package备份文件路径")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间", help_text='修改时间')
    country = models.ForeignKey(Country, verbose_name="国家", help_text='国家')
    offer_url = models.CharField(max_length=200, verbose_name="offer", help_text="offer")
    resc_path = models.CharField(max_length=100, verbose_name="app资源文件路径", help_text="app资源文件路径", blank=True,
                                 null=True)
    offer_id = models.CharField(max_length=50, verbose_name="offer_id", help_text="offer_id", blank=True,
                                 null=True)
    revenue = models.FloatField(default=0, verbose_name="收入", help_text="收入")

    class Meta:
        verbose_name = u'App'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        item = model_to_dict(self)
        return item


class Schedule(models.Model):
    name = models.CharField(max_length=20, verbose_name="name", help_text="name")
    execute_time = models.DateTimeField(max_length=20, verbose_name="执行时间", help_text="执行时间")
    execute_timezone = models.IntegerField(default=8, verbose_name="时区", help_text="时区")
    count = models.IntegerField(default=0, verbose_name="任务数量", help_text="任务数量")
    # script = JSONField(default=list, verbose_name="脚本", help_text="脚本")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    app = models.ForeignKey(App, verbose_name="app", related_name="schedules", help_text='app')
    is_finished = models.BooleanField(default=False, verbose_name="是否完成", help_text="是否完成")

    class Meta:
        verbose_name = u'Schedule'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        item = model_to_dict(self)
        return item


class Script(models.Model):
    schedule = models.ForeignKey(Schedule, verbose_name="关联Schedule", related_name="scripts", help_text='关联Schedule')
    name = models.CharField(max_length=100, verbose_name="脚本名字", help_text="脚本名字")
    path = models.CharField(max_length=100, verbose_name="script path", help_text="script path")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 此脚本下的task完成后就True
    is_finished = models.BooleanField(default=False, verbose_name="是否完成", help_text="是否完成")

    class Meta:
        verbose_name = u'Schedule'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        item = model_to_dict(self)
        return item


class Task(models.Model):
    STEP = (
        (0, 'wait'),
        (1, 'start'),
        (2, 'complete'),
        (3, 'success')
    )
    task_state = models.IntegerField(default=0, choices=STEP, verbose_name='任务状态', help_text='任务状态')
    script = models.ForeignKey(Script, verbose_name="脚本", related_name="task", help_text='task')
    will_recharge = models.BooleanField(default=False, verbose_name="是否充值", help_text="是否充值")
    recharge_amount = models.FloatField(default=0, verbose_name="充值金额", help_text="充值金额")
    phone = models.ForeignKey(Phone, verbose_name="Phone", related_name="tasks", help_text='Phone', blank=True,
                              null=True, )
    pids = JSONField(default=list, verbose_name="进程", help_text='进程')
    config = JSONField(default={}, verbose_name="详细信息", help_text='详细信息')
    # is_finished = models.BooleanField(default=False, verbose_name="是否完成", help_text="是否完成")
    # is_success = models.BooleanField(default=False, verbose_name="是否成功", help_text="是否成功")
    begin_time = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name="任务开始时间",
                                      help_text='任务开始时间')
    end_time = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name="任务结束时间",
                                    help_text='任务结束时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    ref_id = models.CharField(max_length=100, verbose_name="ref_id", help_text="ref_id")
    is_need_reinstall = models.BooleanField(default=False, verbose_name="是否需要重新下载", help_text="是否需要重新下载")
    prev_task = models.ForeignKey('self', blank=True, null=True, verbose_name="上一步流程", related_name="task_next",
                                  help_text='上一步流程')
    package_backup_path = models.CharField(max_length=100, verbose_name="任务备份文件路径", help_text="任务备份文件路径", blank=True,
                                           null=True)
    app_error_log = models.TextField(max_length=100000, verbose_name="app错误日志", blank=True, null=True,
                                     help_text="app错误日志")
    app_info_log = models.TextField(max_length=100000, verbose_name="app日志", blank=True, null=True,
                                    help_text="app日志")
    error_log = models.TextField(max_length=100000, blank=True, null=True, verbose_name="错误日志", help_text="错误日志")
    revenue = models.FloatField(default=0, verbose_name="收入", help_text="收入")
    is_conversion = models.BooleanField(default=False, verbose_name="是否转化", help_text="是否转化")
    is_active = models.BooleanField(default=False, verbose_name="是否激活", help_text="是否激活")
    click_ip = models.CharField(max_length=100, verbose_name="click ip", help_text="click ip", blank=True, null=True)
    @property
    def task_state_str(self):
        return list(self.STEP)[self.task_state][1]

    class Meta:
        verbose_name = u'Task'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}".format(self.pk)

    def to_dict(self):
        item = model_to_dict(self)
        return item


class PostBack(models.Model):
    revenue = models.FloatField(default=0, verbose_name="收入", help_text="收入")
    ref_id = models.CharField(max_length=50, verbose_name="ref_id", blank=True, null=True)
    click_ip = models.CharField(max_length=16, verbose_name="click_ip", blank=True, null=True)
    offer_id = models.CharField(max_length=100, verbose_name="offer_id", blank=True, null=True)

    original = JSONField(default=dict, verbose_name="原始数据")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = u'PostBack'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}-{1}-{2}-{3}".format(self.click_ip, self.ref_id, self.offer_id, self.revenue)


admin.site.register(PostBack)
