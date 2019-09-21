from django.db import models
from django.forms import model_to_dict
# from jsonfield import JSONField
from apps.task.country import Country


class Imgs(models.Model):
    # APP_PLATFORM = {
    #     (0, 'Android'),
    #     (1, 'IOS')
    # }
    # platform = models.IntegerField(default=1, choices=APP_PLATFORM, verbose_name='app类型', help_text='app类型')
    name = models.CharField(max_length=20, verbose_name="图片名字", help_text="图片名字")
    package = models.CharField(max_length=100, verbose_name="图片下载地址", help_text="图片下载地址")

    class Meta:
        verbose_name = u'App'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        item = model_to_dict(self)
        return item



class News(models.Model):
    title = models.CharField(max_length=50, verbose_name="title", help_text="title")
    author = models.CharField(max_length=20, verbose_name="author", help_text="author")
    innerhtml = models.TextField(max_length=3000, verbose_name="文章主体内容", help_text="文章主体内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="文章创建时间", help_text='文章创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name="文章修改时间", help_text='文章修改时间')
    readed_number = models.IntegerField(default=1, verbose_name='阅读数', help_text='阅读数')

    class Meta:
        verbose_name = u'News'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def to_dict(self):
        item = model_to_dict(self)
        return item