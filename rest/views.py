from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from . import utils

def backup_init(request):
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value)
       in request.META.items() if header.startswith('HTTP_'))
    res = {}
    res['type'] = 'init'
    disk = utils.Disk('/dev/sda1')
    avail_space = disk.get_avail_space()
    print(headers['AUTHORIZATION'])
    if headers['AUTHORIZATION'] and Token.objects.get(key=headers['AUTHORIZATION']):

        if avail_space > 1:
            res['status'] = 'ok'
        else:
            res['status'] = 'full_disk'
        res['your_header'] = headers
        return JsonResponse(res)
    else:
        res['error'] = 'Fail Authentication'
        return res



@csrf_exempt
def process_metadata(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        print(received_json_data)
        return JsonResponse(received_json_data)
    else:
        return JsonResponse({"status": "FAILED", "messages": "No data"})


@csrf_exempt
def process_data(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        return JsonResponse(received_json_data)
    else:
        return JsonResponse({"status": "FAILED", "messages": "No data"})