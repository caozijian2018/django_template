import json
import os

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from apps.task.country import Country
from apps.task.models import App, Schedule, Task, Script
from apps.task.rest.filters import ScheduleFilter, ScriptFilter, TaskFilter
from apps.task.rest.serializers import AppCreateSerializer, AppListSerializer, ScheduleCreateSerializer, \
    ScheduleListSerializer, ScheduleEditSerializer, TaskCreateSerializer, TaskEditSerializer, TaskListSerializer, \
    AppEditSerializer, ScriptCreateSerializer, ScriptEditSerializer, ScriptListSerializer, InheritTaskSerializer, \
    CountrySerializer
from apps.utils.utils import CustomPageNumberPagination, LoadsJsonStr, get_file_name, save_file, rename_file, \
    remove_file
from django.conf import settings
import logging

logger = logging.getLogger('__name__')


class AppViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet,
                 LoadsJsonStr):
    queryset = App.objects.all().order_by('-create_time')
    permission_classes = ()
    authentication_classes = ()
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        lists = App.objects.all()
        for item in lists:
            item.name = item.name+"asdasdasd"
        return lists



    def get_serializer_class(self):
        if self.action == 'create':
            return AppCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return AppEditSerializer
        else:
            return AppListSerializer

    # 创建修改app
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # apk
        files = request.FILES.getlist("files")
        file = files[0]
        app_name = get_file_name(file.name)
        file_full_path = save_file(file, settings.APP_FOLDER, app_name)
        # app资源文件 可不传
        resc_files = request.FILES.getlist("resc_file")
        resc_file_full_path = ''
        if len(resc_files):
            resc_file = resc_files[0]
            app_resc_name = get_file_name(resc_file.name)
            resc_file_full_path = save_file(file, settings.APP_RESC_FOLDER, app_resc_name)
            if resc_file_full_path:
                resc_file_full_path = resc_file_full_path[1]
        if file_full_path:
            app_instance = App.objects.create(platform=serializer.validated_data["platform"],
                                              name=serializer.validated_data["name"],
                                              offer_url=serializer.validated_data["offer_url"],
                                              package=file_full_path[1],
                                              package_name=serializer.validated_data["package_name"],
                                              resc_path=resc_file_full_path,
                                              country=serializer.validated_data['country'])

            headers = self.get_success_headers(serializer.data)
            return Response(app_instance.to_dict(), status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        # app
        files = request.FILES.getlist("files")
        if len(files):
            file = files[0]
            app_name = instance.package.split("/")[-1]
            file_full_path = save_file(file, settings.APP_FOLDER, app_name)
            if file_full_path:
                instance.package = file_full_path[1]
                instance.save()
            else:
                err_msg = "上传{}app失败".format(instance.name)
                logger.error(err_msg)
                raise serializers.ValidationError(err_msg)
        # 资源文件
        resc_files = request.FILES.getlist("resc_file")
        if len(resc_files):
            resc_file = resc_files[0]
            app_resc_name = get_file_name(resc_file.name)
            resc_file_full_path = save_file(resc_file, settings.APP_RESC_FOLDER, app_resc_name)
            if resc_file_full_path:
                instance.resc_path = resc_file_full_path[1]
                instance.save()
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ScheduleViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet, UpdateModelMixin,
                      LoadsJsonStr):
    queryset = Schedule.objects.all().order_by('-create_time')
    permission_classes = ()
    authentication_classes = ()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ScheduleFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return ScheduleCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ScheduleEditSerializer
        else:
            return ScheduleListSerializer

    # 创建修改流程
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ScriptViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet, UpdateModelMixin,
                    DestroyModelMixin):
    queryset = Script.objects.all().order_by('-create_time')
    permission_classes = ()
    authentication_classes = ()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ScriptFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return ScriptCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ScriptEditSerializer
        else:
            return ScriptListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 接受scirpt
        schedule = serializer.validated_data['schedule']
        name = serializer.validated_data['name']
        files = request.FILES.getlist("files")
        file = files[0]
        script_name = name + os.path.splitext(file.name)[1]
        # 如果已存在就返回错误
        if schedule.scripts.filter(name=name).count():
            return Response({"msg": "file already exists"}, status=status.HTTP_400_BAD_REQUEST)
        file_full_path = save_file(file, settings.SCRIPT_FOLDER, script_name)
        if file_full_path:
            script_instance = Script.objects.create(schedule=schedule,
                                                    name=name,
                                                    path=file_full_path[1])

            headers = self.get_success_headers(serializer.data)
            return Response(script_instance.to_dict(), status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data['name']
        schedule = instance.schedule
        files = request.FILES.getlist("files")
        if len(files):
            file = files[0]
            script_name = name + os.path.splitext(file.name)[1]
            if schedule.scripts.filter(name=name).exclude(pk=instance.pk).count():
                return Response({"msg": "file already exists"}, status=status.HTTP_400_BAD_REQUEST)
            file_full_path = save_file(file, settings.SCRIPT_FOLDER, script_name, old_file_path=instance.path)
            if file_full_path:
                instance.path = file_full_path[1]
                instance.name = name
                instance.save()
                headers = self.get_success_headers(serializer.data)
                return Response(instance.to_dict(), status=status.HTTP_201_CREATED, headers=headers)
            else:
                err_msg = "上传{}scirpt失败".format(instance.name)
                logger.error(err_msg)
                raise serializers.ValidationError(err_msg)
        else:
            # folder, file_relation_path, new_name
            relation_path = rename_file(settings.SCRIPT_FOLDER, instance.path, name)
            if not relation_path:
                return Response({"msg": "old filt not found!"}, status=status.HTTP_400_BAD_REQUEST)
            instance.path = relation_path[1]
            instance.name = name
            instance.save()
            headers = self.get_success_headers(serializer.data)
            return Response(instance.to_dict(), status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        can_delete = not instance.task.filter(task_state__in=[1, 2, 3]).count()
        if can_delete:
            delete_success = remove_file(instance.path)
            if not delete_success:
                return Response({"msg": "delete script error", "code": 400})
            Task.objects.filter(script=instance).delete()
            instance.delete()
            return Response({"msg": "delete success", "code": 200}, status=status.HTTP_200_OK)
        return Response({"msg": "Script has Task status is not waiting, cannot be deleted", "code": 400},
                        status=status.HTTP_200_OK)


class TaskViewSet(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet,
                  LoadsJsonStr, DestroyModelMixin):
    queryset = Task.objects.all().order_by('-create_time')
    permission_classes = ()
    authentication_classes = ()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = ('create_time',)
    filter_class = TaskFilter
    search_fields = ('ref_id',)

    def get_queryset(self):
        return Task.objects.all().order_by('-create_time')

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return TaskEditSerializer
        else:
            return TaskListSerializer

    # 创建修改流程
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        script = serializer.validated_data['script']
        count = serializer.validated_data['count']
        for i in range(count):
            instance = Task()
            instance.script = script
            instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        hasnext = instance.task_next.filter().count()
        can_delete = instance.task_state == 0 and not hasnext
        if can_delete:
            instance.delete()
            return Response({"msg": "delete success", "code": 200}, status=status.HTTP_200_OK)
        return Response({"msg": "Task cannot be deleted", "code": 400}, status=status.HTTP_200_OK)


class InheritTask(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        :param request: /inherit_task
        :param args:
        :param kwargs: script, task_id_arr [2,3,4]
        :return:
        """
        serializer = InheritTaskSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        script = serializer.validated_data['script']
        task_id_arr = serializer.validated_data['task_id_arr']
        tasks = Task.objects.filter(pk__in=task_id_arr)
        new_task_serializer = []
        for task in tasks:
            new_task = Task()
            new_task.config = task.config
            new_task.package_backup_path = task.package_backup_path
            new_task.ref_id = task.ref_id
            new_task.is_need_reinstall = task.is_need_reinstall
            new_task.prev_task = task
            new_task.script = script
            new_task.save()
            new_task_serializer.append(new_task)
        serializer = TaskListSerializer(new_task_serializer, many=True)
        # headers = self.get_success_headers(new_task_serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CountryView(APIView):
    def get(self, request, *args, **kwargs):
        countries = Country.objects.filter()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
