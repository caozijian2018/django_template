import json
import os

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from apps.task.country import Country
from apps.task.models import Imgs, News
from apps.task.rest.serializers import CountrySerializer, NewsSerializer, ImgsListSerializer, ImgsCreateOrUpdateSerializer
from apps.utils.utils import CustomPageNumberPagination, LoadsJsonStr, get_file_name, save_file, rename_file
from django.conf import settings
import logging

logger = logging.getLogger('__name__')


class NewsViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet,
                  LoadsJsonStr):
    

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    queryset = News.objects.all().order_by('-create_time')
    permission_classes = ()
    authentication_classes = ()
    pagination_class = CustomPageNumberPagination
    serializer_class = NewsSerializer


class ImgsView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get(self, request, *args, **kwargs):
        arr = Imgs.objects.all()
        serializer = ImgsListSerializer(arr, many=True)
        return Response({"imgs": serializer.data}, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        # /site_api/assets/img/ff100202db8811e9a5700242ac1c0003.jpg
        # img/42c0ef3adb8911e99c330242ac1c0003.jpg
        name = request.POST.get("name", "")
        files = request.FILES.getlist("file")
        file = files[0]
        img_name = get_file_name(file.name)
        excel_absolute_path, excel_relative_path = save_file(file, settings.IMGS_FOLDER, img_name)
        if excel_absolute_path:
            try:
                Imgs.objects.create(package=excel_relative_path,name=name)
                return Response({"msg": "ok"}, status=status.HTTP_201_CREATED)
            except:
                return Response({"msg": "fail"}, status=status.HTTP_400_BAD_REQUEST)


# class AppViewSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet,
#                  LoadsJsonStr):
#     queryset = Imgs.objects.all().order_by('-create_time')
#     permission_classes = ()
#     authentication_classes = ()
#     pagination_class = CustomPageNumberPagination

#     def get_queryset(self):
#         lists = App.objects.all()
#         for item in lists:
#             item.name = item.name+"asdasdasd"
#         return lists


#     def get_serializer_class(self):
#         if self.action == 'create':
#             return AppCreateSerializer
#         elif self.action == 'update' or self.action == 'partial_update':
#             return AppEditSerializer
#         else:
#             return AppListSerializer

#     # 创建修改app
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # apk
#         files = request.FILES.getlist("files")
#         file = files[0]
#         app_name = get_file_name(file.name)
#         file_full_path = save_file(file, settings.APP_FOLDER, app_name)
#         # app资源文件 可不传
#         resc_files = request.FILES.getlist("resc_file")
#         resc_file_full_path = ''
#         if len(resc_files):
#             resc_file = resc_files[0]
#             app_resc_name = get_file_name(resc_file.name)
#             resc_file_full_path = save_file(file, settings.APP_RESC_FOLDER, app_resc_name)
#             if resc_file_full_path:
#                 resc_file_full_path = resc_file_full_path[1]
#         if file_full_path:
#             app_instance = App.objects.create(platform=serializer.validated_data["platform"],
#                                               name=serializer.validated_data["name"],
#                                               offer_url=serializer.validated_data["offer_url"],
#                                               package=file_full_path[1],
#                                               package_name=serializer.validated_data["package_name"],
#                                               resc_path=resc_file_full_path,
#                                               country=serializer.validated_data['country'])

#             headers = self.get_success_headers(serializer.data)
#             return Response(app_instance.to_dict(), status=status.HTTP_201_CREATED, headers=headers)
#         else:
#             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # app
#         files = request.FILES.getlist("files")
#         if len(files):
#             file = files[0]
#             app_name = instance.package.split("/")[-1]
#             file_full_path = save_file(file, settings.APP_FOLDER, app_name)
#             if file_full_path:
#                 instance.package = file_full_path[1]
#                 instance.save()
#             else:
#                 err_msg = "上传{}app失败".format(instance.name)
#                 logger.error(err_msg)
#                 raise serializers.ValidationError(err_msg)
#         # 资源文件
#         resc_files = request.FILES.getlist("resc_file")
#         if len(resc_files):
#             resc_file = resc_files[0]
#             app_resc_name = get_file_name(resc_file.name)
#             resc_file_full_path = save_file(resc_file, settings.APP_RESC_FOLDER, app_resc_name)
#             if resc_file_full_path:
#                 instance.resc_path = resc_file_full_path[1]
#                 instance.save()
#         self.perform_update(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CountryView(APIView):
    def get(self, request, *args, **kwargs):
        countries = Country.objects.filter()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
