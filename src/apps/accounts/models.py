import logging

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse_lazy
from rest_framework.exceptions import ValidationError

logger = logging.getLogger("apps.accounts")
STATUS_INACTIVE = 0
STATUS_ACTIVE = 1

ACTIVE_STATUS_CHOICE = ((STATUS_INACTIVE, u'禁用'), (STATUS_ACTIVE, '活跃'))
ACTIVE_STATUS_MAP = dict(ACTIVE_STATUS_CHOICE)
 



class UserManager(models.QuerySet):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def get_by_name_and_domain(self, username, domain):
        return self.get(username=username, company__domain=domain)

    def get_by_full_name(self, full_name):
        return self.get(full_name=full_name)

    def create_user(self, username, company, password, email='', status=True, default_url='', timezone=0):
        if not username or not password or not company:
            return
        try:
            if self.get_by_name_and_domain(username=username, domain=company.domain):
                raise ValidationError(detail={"err_msg": "UNIQUE constraint failed: full_name"})
        except User.DoesNotExist:
            pass

        ins = self.create(username=username, company=company, full_name="%s@%s" % (username, company.domain), email=email, status=status, default_url=default_url, timezone=timezone)
        ins.set_password(password)
        ins.save()

        return ins


    def get_or_none(self, pk):
        try:
            if pk <= 0:
                return None
            return self.get(pk=pk)
        except User.DoesNotExist:
            pass

class User(AbstractBaseUser):
    username = models.CharField(max_length=40, verbose_name="账户名")
    full_name = models.CharField(max_length=200, verbose_name="有域名的账户", unique=True)
    email = models.EmailField(default='')
    status = models.BooleanField(default=True, verbose_name="状态 True启用；False停用", help_text="状态 True启用；False停用",
                                 db_index=True)
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")
    update_dt = models.DateTimeField(auto_now=True, verbose_name="最后一次修改")
    is_superuser = models.BooleanField(default=False, verbose_name="是否为超级用户")
    superuser_level = models.IntegerField(default=0, verbose_name="超级用户级别")
    default_url = models.CharField(max_length=200, default='', verbose_name="默认路径, 默认为空", help_text="默认路径, 默认为空")
    timezone = models.IntegerField(verbose_name="时区, 时区, 从-12到+12", help_text="时区, 从-12到+12", default=0)

    objects = UserManager.as_manager()

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['username']

    @property
    def is_active(self):
        return self.status

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.username

    def first_url(self):
        url_name = self.default_url or 'company:cmp_detail'
        return reverse_lazy(url_name)

    def has_module_perms(self, check_per):
        """
        调用来至template的pers检查
        在界面上不允许公司账户展示其他公司数据。
        界面上的报表数据可以来至多个公司
        :param check_per:
        :return:
        """
        if self.superuser_level == 0:
            return True
        if self.superuser_level == 1:
            return True
        for role in self.roles.filter():
            if isinstance(check_per, (list, set, tuple)):
                if len(role.permission_names().intersection(check_per)):
                    return True
            if check_per in role.permission_names():
                return True
        return False



    def is_global_admin_user(self):
        return self.superuser_level == 0

    def is_company_admin_user(self):
        return self.superuser_level == 1

    def has_company_perms(self, company, per):
        if not company:
            return False
        if self.is_global_admin_user():
            return True
        if self.is_company_admin_user() and self.company.id == company.id:
            return True
        for role in self.roles.filter(company=company):
            if isinstance(per, (list, set, tuple)):
                if len(role.permission_names().intersection(per)):
                    return True
            if per in role.permission_names():
                return True
        return False

    def mark_as_company_manager(self):
        self.superuser_level = 1
        self.save()

    def mark_as_global_manager(self):
        self.superuser_level = 0
        self.save()

    def toggle_status(self):
        if self.status:
            self.status = False
        else:
            self.status = True
        self.save()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s @ %s" % (self.username, self.company.domain)

    def to_dict(self):
        item = model_to_dict(self)
        return item