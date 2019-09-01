import logging
from datetime import datetime
from urllib import parse
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView

from apps.task.models import Task, Script, App, PostBack

logger = logging.getLogger("__name__")


class TaskReportView(APIView):
    def post(self, request, *args, **kwargs):
        params = request.data
        task_id = int(params.get("task_id", 0))

        if not task_id:
            return JsonResponse({"code": 0, "msg": "no task id"})

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return JsonResponse({"code": 0, "msg": "no such task with id = {0}".format(task_id)})

        # 上报pid
        pid = params.get("pid", None)
        if pid:
            task.pids.append(int(pid))
            task.save()
            return JsonResponse({"code": 1, "msg": "ok"})
        # 上报refid
        ref_id = params.get("ref_id", None)
        if ref_id:
            task.ref_id = ref_id
            task.save()
            return JsonResponse({"code": 1, "msg": "ok"})
        #  上报是否激活
        is_active = params.get("is_active", None)
        if is_active is not None:
            task.is_active = is_active
            task.save()
            return JsonResponse({"code": 1, "msg": "ok"})

        # 上报app error log
        app_error_log = params.get("app_error_log", None)
        if app_error_log:
            task.app_error_log = "\n".join(
                (app_error_log, task.app_error_log) if task.app_error_log else (app_error_log,))
            task.save()
            return JsonResponse({"code": 1, "msg": "ok"})

        # 上报app info log
        app_info_log = params.get("app_info_log", None)
        if app_info_log:
            task.app_info_log = "\n".join(
                (app_info_log, task.app_info_log) if task.app_info_log else (app_info_log,))
            task.save()
            return JsonResponse({"code": 1, "msg": "ok"})

        # 上报error log或 success
        error_log = params.get("error_log", None)
        task_state = params.get("task_state", None)
        conf = params.get("conf", None)
        package_backup_path = params.get("package_backup_path", None)
        if error_log:
            task.error_log = "/".join((error_log, task.error_log) if task.error_log else (error_log,))

        else:
            if not conf or not package_backup_path:
                return JsonResponse({"code": 0, "msg": "no config or package_backup_path"})
            task.config = conf
            task.package_backup_path = package_backup_path

        task.task_state = task_state
        task.end_time = datetime.now()
        task.save()
        script_over = len(
            task.script.task.filter(task_state__in=[0, 1])) == 0
        schedule_over = len(
            task.script.schedule.scripts.filter(is_finished=False)) == 0
        script = task.script
        script.is_finished = script_over
        script.save()
        schedule = task.script.schedule
        schedule.is_finished = schedule_over
        schedule.save()
        phone = task.phone
        phone.is_idle = True
        phone.save()

        return JsonResponse({"code": 1, "msg": "ok"})


class PostbackView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            revenue = float(request.GET.get('revenue', 0))
            ref_id = request.GET.get('ref_id', None)
            click_ip = request.GET.get('click_ip', '')
            offer_id = request.GET.get('offer_id', None)
            instance = Task.objects.get(ref_id=ref_id)
            if revenue:
                instance.revenue = revenue
            else:
                revenue = App.objects.get(offer_id=offer_id).revenue
                instance.revenue = revenue
            instance.is_conversion = True
            instance.click_ip = click_ip
            instance.save()
            return JsonResponse({"code": 1, "msg": "ok"})
        except Exception as e:
            logger.error("postback error:{0}".format(str(e)))
            return JsonResponse({"code": 400, "msg": "fail"})


class PostBackViewV2(APIView):
    def get(self, request, *args, **kwargs):
        try:
            revenue = float(request.GET.get('revenue', 0))
            ref_id = request.GET.get('ref_id', None)
            click_ip = request.GET.get('click_ip', '')
            offer_id = request.GET.get('offer_id', None)

            original = {}
            for k in request.GET:
                original[k] = request.GET.get(k, None)
            PostBack.objects.create(revenue=revenue, ref_id=ref_id, click_ip=click_ip, offer_id=offer_id,
                                    original=original)
            return JsonResponse({"code": 1, "msg": "ok"})

        except Exception as e:
            logger.error("postback error:{0}".format(str(e)))
            return JsonResponse({"code": 400, "msg": "fail"})
