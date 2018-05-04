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

STORE_BACKUP_PLACE = "/home/locvu/backup"


def backup_init(request):
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value)
                   in request.META.items() if header.startswith('HTTP_'))
    res = dict()
    res['type'] = 'init'
    # disk = utils.Disk('/dev/sda1')
    # avail_space = disk.get_avail_space()

    avail_space = 2
    try:
        token = headers['AUTHORIZATION']
        tk_obj = Token.objects.get(key=token)
        user = tk_obj.user

        if avail_space > 1:
            res['status'] = 'ok'

            # create repo 
            user = tk_obj.user
            now = datetime.datetime.now()
            repo_name = str(user.username + now.strftime("%Y_%m_%d_%H_%M"))
            store_path = "%s/%s" % (STORE_BACKUP_PLACE, repo_name)
            backup = Backup(user=user, date=now, store_path=store_path)
            backup.save()

            if not os.path.isdir(store_path):
                os.mkdir(store_path)

            res['backup_id'] = backup.id
        else:
            res['status'] = 'full_disk'
        return JsonResponse(res)
    except KeyError:
        return HttpResponse('Unauthorized', status=401)


@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        body = request.body.decode("utf-8")  # convert byte to string 
        print(body)  
        data = json.loads(body)
        # data2 = request.body
        print(data["name"])
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                   in request.META.items() if header.startswith('HTTP_'))
        try:            
            # create folder backup, save info into db
            token = headers['AUTHORIZATION']
            tk_obj = Token.objects.get(key=token)
            current_backup = Backup.objects.get(id= data['backup_id'])
            repo_path = current_backup.store_path

            # process each metadata
            path = repo_path + data['path']
            print(path)
            
            fs = FileSys.objects.get(file_system=data["fs"])

            file_object = File(name=data["name"], type_file=data["type"], path=data["path"], file_system=fs, backup=current_backup)
            file_object.save()
            
            for attribute in data['attr']:
                attr = Attr.objects.get(name=attribute, file_sys=fs)
                attr_value = AttrValue(attr=attr, value=data['attr'][attribute], file_object=file_object)
                attr_value.save()

            if data['type'] == 'directory':
                if not os.path.isdir(path):
                    os.makedirs(path, exist_ok=True)    # make directory recusive
            elif data['type'] == 'file':
                print(path)
                pass
            return JsonResponse(data)
        except KeyError:
            return HttpResponse('Unauthorized', status=401)    
    else:
        return JsonResponse({"status": "FAILED", "messages": "No data"})


@csrf_exempt
def process_data(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        return JsonResponse(received_json_data)
    else:
        return JsonResponse({"status": "FAILED", "messages": "No data"})
