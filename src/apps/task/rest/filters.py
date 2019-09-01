import django_filters
from django.db.models import Q

from apps.task.models import Schedule, Script, Task


class ScheduleFilter(django_filters.rest_framework.FilterSet):
    app = django_filters.CharFilter(label='所属app', method='schedule_app_id_filter', help_text='所属app')

    def schedule_app_id_filter(self, queryset, name, value):
        return queryset.filter(app=value)

    class Meta:
        model = Schedule
        fields = ['app']


class ScriptFilter(django_filters.rest_framework.FilterSet):
    schedule = django_filters.CharFilter(label='所属Schedule', method='script_schedule_id_filter', help_text='所属Schedule')
    pk = django_filters.CharFilter(label='下一步的scirpts', method='next_scripts_filter', help_text='下一步的scripts')

    def script_schedule_id_filter(self, queryset, name, value):
        return queryset.filter(schedule=value)

    def next_scripts_filter(self, queryset, name, value):
        script = queryset.get(pk=value)
        execute_time = script.schedule.execute_time
        try:
            next_schedule_scripts = script.schedule.app.schedules.filter(execute_time__gt=execute_time).order_by(
                'execute_time').first().scripts.all()
            return next_schedule_scripts

        except:
            # bug
            return queryset.filter(pk=-1)

    class Meta:
        model = Script
        fields = ['schedule', 'pk']


class TaskFilter(django_filters.rest_framework.FilterSet):
    script = django_filters.CharFilter(label='所属Script', method='task_script_id_filter', help_text='所属Script')
    schedule = django_filters.CharFilter(label='所属schdule', method='task_schedule_id_filter', help_text='所属schedule')
    state = django_filters.CharFilter(label='task状态', method='task_state_filter',
                                            help_text='task状态')
    app = django_filters.CharFilter(label='app', method='task_app_filter',
                                            help_text='app')

    is_active = django_filters.CharFilter(label='is_active', method='task_is_active_filter',
                                    help_text='is_active')
    is_conversion = django_filters.CharFilter(label='是否转化', method='task_is_conversion_filter',
                                    help_text='是否转化')

    def task_script_id_filter(self, queryset, name, value):
        return queryset.filter(script=value)

    def task_schedule_id_filter(self, queryset, name, value):
        return queryset.filter(script__schedule=value)

    def task_state_filter(self, queryset, name, value):
        return queryset.filter(task_state=int(value))

    def task_app_filter(self, queryset, name, value):
        return queryset.filter(script__schedule__app=value)

    def task_is_active_filter(self, queryset, name, value):
        return queryset.filter(is_active=(value == 'true'))

    def task_is_conversion_filter(self, queryset, name, value):
        return queryset.filter(is_conversion=(value == 'true'))

    class Meta:
        model = Task
        fields = ['script', 'schedule', 'state']
