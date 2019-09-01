# _*_ encoding: utf-8 _*_
import socket
import sys
import os
import argparse
import traceback
import time
import hashlib
from ftplib import FTP

parser = argparse.ArgumentParser()
parser.add_argument("--settings")
args = parser.parse_args()
settings = 'settings.prod' if not args.settings else args.settings

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, pwd + "/../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

import django

django.setup()

import logging
from datetime import datetime, timedelta

import requests
from requests.adapters import HTTPAdapter
from django.conf import settings
from apps.task.models import Schedule, Task
from apps.device.models import Phone

req_s = requests.Session()
req_s.mount('http://', HTTPAdapter(max_retries=10))
req_s.mount('https://', HTTPAdapter(max_retries=10))
logger = logging.getLogger("__name__")


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    except:
        logger.error(traceback.format_exc())
    finally:
        s.close()


def remove_list_dup_dict(tmp):
    return [dict(t) for t in set([tuple(d.items()) for d in tmp])]


def get_schedules():
    try:
        ret = []
        utc_now = datetime.utcnow()
        schedules = Schedule.objects.filter(is_finished=False).order_by('execute_time')
        for schedule in schedules:
            if schedule.execute_time <= utc_now + timedelta(hours=schedule.execute_timezone):
                ret.append(schedule)
        return ret
    except:
        logger.error("get schedules error:{0}".format(traceback.format_exc()))
        return []


def call_api(url, params):
    resp = req_s.post(url=url, json=params)
    logger.info("call api: {0}--{1}--{2}".format(url, params, resp.json()))
    if resp.status_code == 200 and int(resp.json()["code"]) == 1:
        return True
    return False


def get_file_md5(file_path):
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        md5.update(f.read())
        _hash = md5.hexdigest()
    return str(_hash).upper()


def get_ftp_file_md5(src_ip, file_path):
    with FTP(host=src_ip, user=settings.FTP_USER, passwd=settings.FTP_PWD)as ftp:
        ftp.encoding = 'utf-8'
        if "/" in file_path and not file_path.startswith("/"):
            _src_path = "/" + file_path
        else:
            _src_path = file_path
        with open(_src_path, 'wb') as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            _hash = md5.hexdigest()
        return str(_hash).upper()


def trans_script(src_ip, slave_ip, task_id, script):
    try:
        url = "http://{slave_ip}:{port}/trans/script/".format(slave_ip=slave_ip, port=settings.SLAVE_PORT)
        full_src_path = settings.FILE_PATH_PREFIX + script.path
        md5 = get_file_md5(full_src_path)
        params = [{"task_id": task_id, "src_ip": src_ip, "src_path": script.path, "dst_path": script.path, "md5": md5}]
        print(params)
        s = call_api(url, params)
        print(s)
        return s
    except:
        logger.error("deploy script error:{0}".format(traceback.format_exc()))
        print("deploy script error:{0}".format(traceback.format_exc()))
        return False


def trans_app(src_ip, slave_ip, task_id, app):
    try:
        url = "http://{slave_ip}:{port}/trans/app/".format(slave_ip=slave_ip, port=settings.SLAVE_PORT)
        full_src_path = os.path.join(settings.FILE_PATH_PREFIX, app.package)
        md5 = get_file_md5(full_src_path)
        params = [{"task_id": task_id, "src_ip": src_ip, "src_path": app.package, "dst_path": app.package, "md5": md5}]
        if app.resc_path:
            full_resc_path = os.path.join(settings.FILE_PATH_PREFIX, app.resc_path)
            md5 = get_file_md5(full_resc_path)
            params.append({"task_id": task_id, "src_ip": src_ip, "src_path": app.resc_path, "dst_path": app.resc_path, "md5": md5})
        return call_api(url, params)
    except:
        logger.error("deploy app error:{0}".format(traceback.format_exc()))
        return False


def trans_backup_files(src_ip, slave_ip, src_task, dst_task):
    try:
        if not src_task.package_backup_path:
            return True
        if src_ip == slave_ip:
            return True
        url = "http://{slave_ip}:{port}/trans/backup/".format(slave_ip=slave_ip, port=settings.SLAVE_PORT)
        full_src_path = os.path.join(settings.FILE_PATH_PREFIX, src_task.package_backup_path)
        md5 = get_ftp_file_md5(src_ip, full_src_path)
        params = [{"task_id": dst_task.id, "src_ip": src_ip, "src_path": src_task.package_backup_path,
                   "dst_path": dst_task.package_backup_path, "md5": md5}]
        return call_api(url, params)
    except:
        logger.error("deploy backup files error:{0}".format(traceback.format_exc()))
        return False


def run_task(slave_ip, task, app, phone, script):
    try:
        url = "http://{slave_ip}:{port}/task/do_task/".format(slave_ip=slave_ip, port=settings.SLAVE_PORT)
        params = {"task_id": task.id, "udid": phone.uuid, "package_name": app.package_name,
                  "is_need_reinstall": task.is_need_reinstall, "script_name": task.script.name,
                  "will_recharge": task.will_recharge, "recharge_amount": task.recharge_amount, "ref_id": task.ref_id,
                  "offer_url": app.offer_url, "config": task.config, "local_package_path": app.package,
                  "local_backup_path": task.package_backup_path, "local_script_path": script.path,
                  "local_resc_path": app.resc_path}
        return call_api(url, params)
    except:
        logger.error("run task error:{0}".format(traceback.format_exc()))
        return False


def main():
    try:
        while True:
            schedules = get_schedules()
            for schedule in schedules:
                tasks = Task.objects.filter(script__schedule=schedule, task_state=0)
                for task in tasks:
                    phone_filter_p = {"country": schedule.app.country, "is_idle": True, "is_stop": False, "status": 0}
                    if task.will_recharge:
                        phone_filter_p["can_recharge"] = True
                    phone = Phone.objects.filter(**phone_filter_p).first()
                    if not phone:
                        continue
                    src_ip = get_host_ip()
                    slave = phone.slave
                    app = schedule.app
                    script = task.script
                    print(task.to_dict())
                    ret_script = trans_script(src_ip, slave.ip, task.id, script)
                    ret_app = trans_app(src_ip, slave.ip, task.id, app)
                    ret_backup = trans_backup_files(task.prev_task.phone.slave.ip, slave.ip, task.prev_task, task) if task.prev_task else True
                    print(ret_script, ret_backup)
                    if ret_script and ret_app and ret_backup:
                        if run_task(slave.ip, task, app, phone, script):
                            # mark task and phone
                            task.task_state = 1
                            task.phone = phone
                            task.begin_time = datetime.now()
                            task.save()
                            phone.is_idle = False
                            phone.save()
            time.sleep(settings.RUN_SCHEDULE_TIMEOUT)
    except:
        logger.error("run schedule error: {0}".format(traceback.format_exc()))


if __name__ == "__main__":
    main()
