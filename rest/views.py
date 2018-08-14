import os
import re
import datetime
import json
import subprocess
import logging
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from cryptography.fernet import Fernet

from . import utils
from .models import Backup, File, FileSys, FileData, Attr, AttrValue
from .serializers import DataSerializer
from djangorest import settings


logger = logging.getLogger(__name__)


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
    except (Token.DoesNotExist, KeyError):
        return None


def backup_init(request):
    res = dict()
    res['type'] = 'init'
    # disk = utils.Disk('/dev/sda1')
    # avail_space = disk.get_avail_space()

    avail_space = 2  # for test 
    user = get_user_by_token(request)
    if user:
        if avail_space > settings.MIN_CAPACITY:  # Available storage greater than 1 GB
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
            print(res)
            return JsonResponse(res)    # return 200
        else:
            return HttpResponse('Full disk', status=507)
    else:
        return HttpResponse('Unauthorized', status=401)


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

    # Compare previous version
    tupple_id_checksum = checksum_pre_version(user, request_data['path'])    # (id, checksum)
    for checksum in request_data['checksum']:
        if tupple_id_checksum:
            for data_id, cks in tupple_id_checksum:  # block data existed
                if checksum == cks:
                    block_data = FileData.objects.get(id=data_id).block_data
                    filedata = FileData(block_data=block_data, block_id=block_id,
                                        checksum=checksum, file_object=file_object)
                    filedata.save()
                    break
            else:                               # receive data
                blk_list.append(block_id)
                cks_list.append(checksum)
            block_id += 1
        else:   # the first version
            blk_list = list(range(len(request_data['checksum'])))
            cks_list = request_data['checksum']

    response_data['blocks'] = blk_list
    response_data['checksum'] = cks_list
    return response_data


@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        user = get_user_by_token(request)
        if user:
            cipher_suite = Fernet(user.keyuser.key)
            plain_text = cipher_suite.decrypt(request.body)
            request_data = json.loads(plain_text.decode())
            print(request_data)
            current_backup = Backup.objects.get(id=request_data['backup_id'])
            repo_path = current_backup.store_path
            path = repo_path + request_data['path']

            # create a file object
            try:
                fs = FileSys.objects.get(file_system=request_data["fs"])
            except FileSys.DoesNotExist:
                fs = FileSys.objects.create(file_system=request_data["fs"])

            file_object = File(name=request_data["name"], type_file=request_data["type"],
                            path=request_data["path"], file_system=fs, backup=current_backup)
            file_object.save()

            # create attr objects
            for attribute in request_data['attr']:
                try:
                    attr = Attr.objects.get(name=attribute, file_sys=fs)
                except Attr.DoesNotExist:
                    attr = Attr.objects.create(name=attribute, file_sys=fs)

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
            print(response_data)
            cipher_text = cipher_suite.encrypt(json.dumps(response_data).encode())
            return HttpResponse(cipher_text, content_type='application/octet-stream')
        else:
            return HttpResponse('Unauthorized', status=401)


class DataView(APIView):
    """
        Receive data and store in storage
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        user = get_user_by_token(request)
        if user:
        # decrypt
        # cipher_suite = Fernet(user.keyuser.key)
        # print(request.FILES.getlist('block_data'))

            data_serializer = DataSerializer(data=request.data)
            if data_serializer.is_valid():
                data_serializer.save()
                return Response(data_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse('Unauthorized', status=401)

    def get(self, request, *args, **ksargs):
        pass


def list_backup_info(request, pk=None):
    if request.method == 'GET':
        user = get_user_by_token(request)
        if user:
            response_data = {}
            if pk:
                try:
                    backup = Backup.objects.get(user=user, pk=pk)
                    name = backup.store_path[len(settings.UPLOAD_ROOT):]
                    response_data = {'pk': backup.pk, 'date': backup.date, 'name': name}
                except Backup.DoesNotExist:
                    return HttpResponse('DoesNotExist', status=404)
            else:
                backup = Backup.objects.filter(user=user)
                values = backup.values('pk', 'date', 'store_path')
                count = 0
                for value in values:
                    name = value['store_path'][len(settings.UPLOAD_ROOT):]
                    response_data[count] = {'pk': value['pk'], 'date': value['date'], 'name': name}
                    count += 1
            return JsonResponse(response_data)
        else:
            return HttpResponse('Unauthorized', status=401)


def restore_init(request, version=None):
    if request.method == 'GET':
        user = get_user_by_token(request)
        
        if version:
            try:
                path = request.GET.get('path')
                # print(version)
                logger.debug(path)
                backup = Backup.objects.filter(user=user)[int(version)]
                files = File.objects.filter(backup=backup, path__startswith=path)
                if files:
                    response_data = {}
                    for f in files: 
                        attr_set = f.attrvalue_set.all()
                        attr = {a.attr.name: a.value for a in attr_set}
                        response_data[f.pk] = {'name': f.name, 'path': f.path, 'type': f.type_file,
                                               'fs': str(f.file_system), 'attr': attr}
                        if f.type_file == 'file':
                            response_data[f.pk].update({'checksum': list(f.filedata_set.values_list('checksum', flat=True))})
                    return JsonResponse(response_data)
                else:
                    return HttpResponse('Path Does Not Exist', status=404)

            except IndexError:
                return HttpResponse('Version Does Not Exist', status=404)
        else:
            return HttpResponse("Missing version definite", status=412)


@csrf_exempt
def download_data(request, version=None):
    if request.method == 'GET':
        user = get_user_by_token(request)
        if user:
            if version:
                try:
                    body = request.body.decode("utf-8")  # convert byte to string
                    print(body)
                    request_data = json.loads(body)

                    # data = FileData.objects.get(file_object=f, checksum=checksum)
                    url = url_by_checksum(user, version, request_data['path'],
                                        request_data['need'].values())
                    response_data = request_data
                    print(url)
                    response_data['url'] = url
                    print(response_data)
                    return JsonResponse(response_data)
                except IndexError:
                    return HttpResponse('Version Does Not Exist', status=404)
            else:
                return HttpResponse("Missing version definite", status=412)
        else:
            return HttpResponse('Unauthorized', status=401)


def url_by_checksum(user, version, path, list_checksum):
    backup = Backup.objects.filter(user=user)[int(version)]
    f = File.objects.get(backup=backup, path=path)
    datas = FileData.objects.filter(file_object=f, checksum__in=list_checksum)
    url = {}
    for data in datas:
        url[str(data.block_id)] = data.block_data.url

    return url 


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        body = request.body.decode("utf-8")  # convert byte to string
        request_data = json.loads(body)
        print(request_data)
        username = request_data['username']
        password = "strongpass@@"

        # Check username existed 
        try: 
            user = User.objects.get(username=username)
            return HttpResponse('Create agent fail: User ' + username + ' existed', status=409)
        except User.DoesNotExist:
            user = User(username=username, password=password)
            user.save()
            token = Token(user=user)
            token.save()
            crypt_key = user.keyuser.key 

            return JsonResponse({"token": token.key, "key": crypt_key})


def list_user(request):
    if request.method == "GET":
        users = User.object.all()
        user_data = {}
        for user in users:
            user_data[user.pk] = user.username
        return JsonResponse(user_data)


@csrf_exempt
def remove_user(request):
    if request.method == 'POST':
        body = request.body.decode("utf-8")
        request_data = json.loads(body)
        username = request_data['username']
        user = User.objects.get(username=username)
        user.delete()
        return HttpResponse('User Deleted', status=200)


def result_backup(request, backup_id):
    if request.method == 'GET':
        user = get_user_by_token(request)
        if user:
            backup = Backup.objects.get(user=user, pk=backup_id)
            size_dir = subprocess.check_output(['du','-sb', backup.store_path]).split()[0].decode('utf-8')
            return JsonResponse({"data_change": size_dir, "sync_time": backup.date})
        else:
            return HttpResponse('Unauthorized', status=401)
