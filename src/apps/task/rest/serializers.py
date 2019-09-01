# -*- coding: utf-8 -*-
from rest_framework import serializers

from apps.task.country import Country
from apps.task.models import App, Schedule, Task, Script


class AppCreateSerializer(serializers.ModelSerializer):
    files = serializers.FileField()

    class Meta:
        model = App
        exclude = ('create_time', 'update_time', 'package', 'resc_path', 'package_backup_path')


class AppEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        exclude = ('create_time', 'update_time', 'package', 'resc_path', 'package_backup_path')


class AppListSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()

    def get_country_name(self, app):
        return app.country.name

    class Meta:
        model = App
        fields = '__all__'


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('name', 'execute_time', 'execute_timezone', 'count', 'app')


class ScheduleEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('name', 'execute_time', 'execute_timezone', 'count')


class ScheduleListSerializer(serializers.ModelSerializer):
    complate = serializers.SerializerMethodField()

    def get_complate(self, schedule):
        scripts = schedule.scripts.filter()
        complate_num = 0
        for script in scripts:
            complate_num += script.task.filter(task_state__in=[2, 3]).count()
        return complate_num

    def get_script(self, schedule):
        return schedule.script

    class Meta:
        model = Schedule
        fields = '__all__'


class ScriptCreateSerializer(serializers.ModelSerializer):
    files = serializers.FileField()

    class Meta:
        model = Script
        fields = ('files', 'schedule', 'name')


class ScriptEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Script
        fields = ('name',)


class ScriptListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Task
        fields = ("script", "count")


class TaskEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("will_recharge", "recharge_amount", "config")


class TaskListSerializer(serializers.ModelSerializer):
    script = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    pids = serializers.JSONField()
    slave = serializers.SerializerMethodField()
    task_state = serializers.SerializerMethodField()
    schedule = serializers.SerializerMethodField()
    task_has_next = serializers.SerializerMethodField()

    def get_script(self, task):
        return task.script.to_dict()

    def get_slave(self, task):
        try:
            return task.phone.slave.to_dict() if task.phone.slave else None
        except:
            return None

    def get_phone(self, task):
        return task.phone.to_dict() if task.phone else None

    def get_task_state(self, task):
        return Task.STEP[task.task_state][1]

    def get_schedule(self, task):
        return task.script.schedule.to_dict()

    def get_task_has_next(self, task):
        return True if task.task_next.filter().count() else False


    class Meta:
        model = Task
        fields = "__all__"


class InheritTaskSerializer(serializers.ModelSerializer):
    task_id_arr = serializers.JSONField()

    class Meta:
        model = Task
        fields = ("script", "task_id_arr")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
