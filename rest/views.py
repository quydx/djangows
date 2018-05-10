import os
import re
import datetime
import json
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from . import utils
from .models import Backup, File, FileSys, FileData, Attr, AttrValue
from .serializers import DataSerializer

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
        print(token)
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


def checksum_pre_version(user, path):
    try:
        f = File.objects.filter(path=path, backup__user=user)
        if f.count() < 2:
            return None
        else:
            f = f[f.count()-2]      # latest - 1 
            checksumlist = f.filedata_set.values_list('id', 'checksum')
            return checksumlist
    except File.DoesNotExist:
        return None

# sample result
# (442, '3cedbef3e8123e04dcfa9076ffd5f95a')
# (443, '90fa3f358103a5d183fa54d5b07940e0')
# (444, 'a3952428d4a238112b2dd10a415af94c')
# (445, '1f1825604f7d9ec6f84fa74053c91887')
# (446, '0a9f6ee45eaa472c55ad24755c0f165d')
# (447, '2bb875ee749c8cf6636845a418401c6f')
# (448, '5d8272e3a4c3ad8bbb5348adb67dd7a9')
# (449, 'facfbba53963b8e44b06e9edf9c1764d')
# (450, '14600c3f5d351c2d5aa3ecd4ee139238')


@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        body = request.body.decode("utf-8")  # convert byte to string 
        # print(body)  
        request_data = json.loads(body)
        # data2 = request.body
        print(request_data["name"])
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                   in request.META.items() if header.startswith('HTTP_'))
        try:            
            # create folder backup, save info into db
            token = headers['AUTHORIZATION']
            tk_obj = Token.objects.get(key=token)
            user = tk_obj.user
            current_backup = Backup.objects.get(id=request_data['backup_id'])
            repo_path = current_backup.store_path

            # process each metadata
            path = repo_path + request_data['path']
            print(request_data)   
            fs = FileSys.objects.get(file_system=request_data["fs"])

            file_object = File(name=request_data["name"], type_file=request_data["type"], path=request_data["path"], file_system=fs, backup=current_backup)
            file_object.save()
            
            for attribute in request_data['attr']:
                attr = Attr.objects.get(name=attribute, file_sys=fs)
                attr_value = AttrValue(attr=attr, value=request_data['attr'][attribute], file_object=file_object)
                attr_value.save()
            response_data = {}
           
            if request_data['type'] == 'directory':
                if not os.path.isdir(path):
                    os.makedirs(path, exist_ok=True)    # make directory recusive
            elif request_data['type'] == 'file' and request_data['checksum'] != []:
                # data sample
                # request_data = {"type": "file", 
                #       "attr": {"modify_time": 1515229034.767711, "create_time": 1521355529.0271544, 
                #               "nlink": 1, "mode": 33279, "device": 2050, "uid": 1000, "size": 8416, 
                #               "access_time": 1525882399.384772, "inode": 6031529, "gid": 1000}, 
                #       "fs": "ext4", 
                #       "path": "/home/locvu/openvpn-ca/openssl-0.9.8.cnf", 
                #       "name": "openssl-0.9.8.cnf", 
                #       "backup_id": 80, 
                #       "checksum": ["3cedbef3e8123e04dcfa9076ffd5f95a", "90fa3f358103a5d183fa54d5b07940e0", "a3952428d4a238112b2dd10a415af94c", "1f1825604f7d9ec6f84fa74053c91887", "0a9f6ee45eaa472c55ad24755c0f165d", "2bb875ee749c8cf6636845a418401c6f", "5d8272e3a4c3ad8bbb5348adb67dd7a9", "facfbba53963b8e44b06e9edf9c1764d", "14600c3f5d351c2d5aa3ecd4ee139238"]}
                
                response_data['file_object'] = file_object.pk
                
                blk_list = []
                cks_list = []
                block_id = 0
                
                tupple_id_checksum = checksum_pre_version(user, request_data['path'])    # (id, checksum)
                print(response_data)
                for checksum in request_data['checksum']:
                    if tupple_id_checksum:
                        for data_id, cks in tupple_id_checksum:  # block data existed
                            if checksum == cks: 
                                block_data = FileData.objects.get(id=data_id).block_data 
                                filedata = FileData(block_data=block_data, block_id=block_id, checksum=checksum, file_object=file_object)
                                filedata.save()
                                break;
                        else:                         # receive data
                            blk_list.append(block_id)
                            cks_list.append(checksum)
                        block_id += 1    
                    else:   # the first version 
                        blk_list = list(range(len(request_data['checksum'])))
                        cks_list = request_data['checksum']
                        
                response_data['blocks'] = blk_list
                response_data['checksum'] = cks_list

            response_data['status'] = "SUCCESS" 
            print("RESPONSE DAAAAAD")   
            print(response_data)
            return JsonResponse(response_data)
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


class DataView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        data = request.data 
        print(request.data)
        # data['file_object'] = File.objects.get(pk=data['file_pk'])
        # data.pop('file_pk', None)
        print(data)
        
        # return Response("ok", status=status.HTTP_201_CREATED) 
        data_serializer = DataSerializer(data=data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
