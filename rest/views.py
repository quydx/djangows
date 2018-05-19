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
from djangorest import settings


def get_header(request):
    regex = re.compile('^HTTP_')
    header = dict((regex.sub('', header), value) for (header, value)
                   in request.META.items() if header.startswith('HTTP_'))
    return header


def get_user_by_token(request):
    header = get_header(request)
    try:
        token = header['AUTHORIZATION']
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        return user
    except Token.DoesNotExist:
        return HttpResponse('Token is not authorized', status=401)
    except KeyError:
        return HttpResponse('Unauthorized', status=401)


def backup_init(request):
    res = dict()
    res['type'] = 'init'
    # disk = utils.Disk('/dev/sda1')
    # avail_space = disk.get_avail_space()

    avail_space = 2
    user = get_user_by_token(request)

    if avail_space > 1:
        # create repo
        now = datetime.datetime.now()
        repo_name = str(user.username + now.strftime("%Y_%m_%d_%H_%M"))
        store_path = "{}{}".format(settings.UPLOAD_ROOT, repo_name)
        backup = Backup(user=user, date=now, store_path=store_path)
        backup.save()

        # make dir repo
        if not os.path.isdir(store_path):
            os.mkdir(store_path)

        res['status'] = 'ok'
        res['backup_id'] = backup.id
        return JsonResponse(res)    # return 200
    else:
        return HttpResponse('Full disk', status=507)
    

def checksum_pre_version(user, path):
    try:
        f = File.objects.filter(path=path, backup__user=user)
        if f.count() < 2:           # the first version 
            return None
        else:
            f = f[f.count()-2]      # latest - 1 
            checksumlist = f.filedata_set.values_list('id', 'checksum')
            return checksumlist
    except File.DoesNotExist:
        return None


def process_filedata(file_object, request_data, user):
    response_data = {'file_object': file_object.pk}    
    blk_list, cks_list = [], []
    block_id = 0
    
    tupple_id_checksum = checksum_pre_version(user, request_data['path'])    # (id, checksum)
    for checksum in request_data['checksum']:
        if tupple_id_checksum:
            for data_id, cks in tupple_id_checksum:  # block data existed
                if checksum == cks: 
                    block_data = FileData.objects.get(id=data_id).block_data 
                    filedata = FileData(block_data=block_data, block_id=block_id, checksum=checksum, file_object=file_object)
                    filedata.save()
                    break;
            else:                               # receive data
                blk_list.append(block_id)
                cks_list.append(checksum)
            block_id += 1    
        else:   # the first version 
            blk_list = list(range(len(request_data['checksum'])))
            cks_list = request_data['checksum']

    response_data['blocks'] = blk_list
    response_data['checksum'] = cks_list
    return request_data


@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        body = request.body.decode("utf-8")  # convert byte to string  
        request_data = json.loads(body)
        current_backup = Backup.objects.get(id=request_data['backup_id'])
        repo_path = current_backup.store_path
        path = repo_path + request_data['path']
        user = get_user_by_token(request)

        # create a file object   
        fs = FileSys.objects.get(file_system=request_data["fs"])
        file_object = File(name=request_data["name"], type_file=request_data["type"], path=request_data["path"], file_system=fs, backup=current_backup)
        file_object.save()
        
        # create attr objects
        for attribute in request_data['attr']:
            attr = Attr.objects.get(name=attribute, file_sys=fs)
            attr_value = AttrValue(attr=attr, value=request_data['attr'][attribute], file_object=file_object)
            attr_value.save()
            
        response_data = {}
        
        if request_data['type'] == 'directory':
            if not os.path.isdir(path):
                os.makedirs(path, exist_ok=True)    # make directory recusive
        elif request_data['type'] == 'file' and request_data['checksum'] != []:
            response_filedata = process_filedata(file_object, request_data, user)
            response_data.update(response_filedata)

        response_data['status'] = "SUCCESS" 
        return JsonResponse(response_data) 
    else:
        return JsonResponse({"status": "FAILED", "messages": "No data"})

    
class DataView(APIView):
    """
        Receive data and store in storage 
    """
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        data = request.data 
        data_serializer = DataSerializer(data=data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def list_backup_info(request, pk=None):
    if request.method == 'GET':
        user = get_user_by_token(request)
        response_data = {}
        if pk:
            try:
                backup = Backup.objects.get(user=user, pk=pk)
                name = backup.store_path[len(settings.UPLOAD_ROOT):]
                response_data = {'pk': backup.pk, 'date': backup.date, 'name':name}
            except Backup.DoesNotExist:
                return HttpResponse('DoesNotExist', status=404)    
        else:
            backup = Backup.objects.filter(user=user)
            values = backup.values('pk', 'date', 'store_path')
            count = 0 
            for value in values:
                name = value['store_path'][len(settings.UPLOAD_ROOT):]
                response_data[count] = {'pk': value['pk'], 'date': value['date'], 'name':name}
                count += 1
        return JsonResponse(response_data)
