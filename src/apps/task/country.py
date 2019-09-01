from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=50, default="", verbose_name="国家名称")
    code = models.CharField(max_length=10, default="", verbose_name="国家简称")
    rate = models.FloatField(null=True, blank=True, verbose_name="汇率", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新日期")

    class Meta:
        verbose_name = u"国家"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}【{1}】'.format(self.code, self.name)