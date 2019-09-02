from django.db import models
from django.forms import model_to_dict
# from jsonfield import JSONField
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

