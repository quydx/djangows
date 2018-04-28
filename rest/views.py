from django.shortcuts import render

# Create your views here.
from .models import *
import json
from django.http import HttpResponse
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt
import os
from rest_framework.authtoken.models import Token
from pprint import pprint
import datetime
from . import utils

STORE_BACKUP_PLACE = "/opt/backup"


def backup_init(request):
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value)
                   in request.META.items() if header.startswith('HTTP_'))
    res = dict()
    res['type'] = 'init'
    # disk = utils.Disk('/dev/sda1')
    # avail_space = disk.get_avail_space()
    print(headers['AUTHORIZATION'])
    avail_space = 2
    token = headers['AUTHORIZATION']
    tk_obj = Token.objects.get(key=token)
    user = tk_obj.user
    pass_backups = user.backup_set.all()
    res['type'] = 'full' if not pass_backups else 'increament'
    if not user:
        return HttpResponse('Unauthorized', status=401)
    if avail_space > 1:
        res['status'] = 'ok'
    else:
        res['status'] = 'full_disk'
    return JsonResponse(res)


@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # create folder backup, save info into db
        tk_obj = Token.objects.get(key=data['token'])
        user = tk_obj.user
        now = datetime.datetime.now()
        folder_name = str(user.username + now.strftime("%Y_%m_%d_%H_%M"))
        store_path = "%s/%s" % (STORE_BACKUP_PLACE, folder_name)
        backup = Backup(user=user, date=now, store_path=store_path)
        backup.save()
        if not os.path.isdir(store_path):
            os.mkdir(store_path)

        # process each metadata
        if data['type'] == 'folder':
            if not os.path.isdir(data['path']):
                # os.mkdir(backup_folder + path)
                print('backupfolder: ' + folder_name + '/' + data['path'])

        elif data['type'] == 'file':
            # file_attrs = data['file_attrs']
            pass

        return JsonResponse(data)
    else:
        return JsonResponse({"status": "FAILED", "messages": "No data"})


@csrf_exempt
def process_data(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        return JsonResponse(received_json_data)
    else:
        return JsonResponse({"status": "FAILED", "messages": "No data"})
