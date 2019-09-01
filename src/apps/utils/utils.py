# -*- coding: utf-8 -*-
import json
import os
import uuid

from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 12
    page_size_query_param = 'capacity'
    max_page_size = 10000


class LoadsJsonStr(object):
    def serializer_loads_script(self, serializer, attr_names):
        def serializer_single_loads(serializer, attr_name):
            attr = serializer.validated_data.get(attr_name, None)
            if attr:
                serializer.validated_data[attr_name] = json.loads(attr)

        if isinstance(attr_names, list):
            for attr_name in attr_names:
                serializer_single_loads(serializer, attr_name)
        else:
            serializer_single_loads(serializer, attr_names)


def get_uuid():
    return str(uuid.uuid1()).replace('-', '')


def get_file_name(filename):
    file_suffix = filename.split('.')[-1]
    file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_suffix
    return file_name


def save_file(file, folder, filename=None, old_file_path=None):
    try:
        # 如果oldfile 那么存下新的删掉旧的
        if filename:
            file_name = filename.replace(' ', '').strip()
            file_full_path = os.path.join(os.path.join(settings.FILE_PATH_PREFIX, folder), file_name)
        else:
            file_name = file.name.replace(' ', '').strip()
            file_full_path = os.path.join(os.path.join(settings.FILE_PATH_PREFIX, folder), file_name)
        with open(file_full_path, 'wb+') as f:
            try:
                for chunk in file.chunks():
                    f.write(chunk)
                file_relation_path = os.path.join(folder, file_name)
                if old_file_path:
                    try:
                        os.remove(os.path.join(settings.FILE_PATH_PREFIX, old_file_path))
                    except:
                        pass
                return file_full_path, file_relation_path
            except AttributeError:
                for chunk in file.iter_content(chunk_size=128):
                    f.write(chunk)
                return False
    except Exception as e:
        print(e)
        return False


def rename_file(folder, file_relation_path, new_name):
    try:
        new_relation_path = os.path.join(folder, new_name + os.path.splitext(file_relation_path)[1])
        file_old_path = os.path.join(settings.FILE_PATH_PREFIX, file_relation_path)
        file_new_path = os.path.join(settings.FILE_PATH_PREFIX, new_relation_path)
        os.rename(file_old_path, file_new_path)
        return file_new_path, new_relation_path
    except Exception as e:
        print(e)
        return False


def remove_file(file_relation_path):
    try:
        file_path = os.path.join(settings.FILE_PATH_PREFIX, file_relation_path)
        os.remove(file_path)
        return True
    except Exception as e:
        print(e)
        return False