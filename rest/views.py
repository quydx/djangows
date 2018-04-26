from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt
import os
from . import utils


def backup_init(request):
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value)
       in request.META.items() if header.startswith('HTTP_'))
    res = {}
    res['type'] = 'init'
    disk = utils.Disk('/dev/sda1')
    avail_space = disk.get_avail_space()
    if avail_space > 1:
        res['status'] = 'ok'
    else:
        res['status'] = 'full_disk'
    res['your_header'] = headers
    return JsonResponse(res)


@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        path = data['path']
        if data['type'] == 'folder':
            if not os.path.isdir(path):
                backup_folder = 'somefolder'
                # os.mkdir(backup_folder + path)
                print('backupfolder: ' + backup_folder + '/' + path)
        elif data['type'] == 'file':
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