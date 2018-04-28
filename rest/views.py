from django.shortcuts import render

# Create your views here.
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


def backup_init(request):
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value)
       in request.META.items() if header.startswith('HTTP_'))
    res = {}
    res['type'] = 'init'
    pprint(headers)
    # disk = utils.Disk('/dev/sda1')
    # avail_space = disk.get_avail_space()
    print(headers['AUTHORIZATION'])
    avail_space = 2
    try:
        token = headers['AUTHORIZATION']
        tk = Token.objects.get(key=token)
        pprint(tk)
        if avail_space > 1 and tk:
            res['status'] = 'ok'
        else:
            res['status'] = 'full_disk'
        res['your_header'] = headers
        return JsonResponse(res)
    except KeyError:
        return HttpResponse('Unauthorized', status=401)


@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data['token']
        tk_obj = Token.objects.get(key=token)
        user = tk_obj.user
        pprint('user = ' + user.username)
        now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        folder_name = str(user.username + now)
        print(folder_name)
        path = data['path']
        if data['type'] == 'folder':
            if not os.path.isdir(path):
                # os.mkdir(backup_folder + path)
                print('backupfolder: ' + folder_name + '/' + path)

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