from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponse
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt


def backup_init(request):
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value)
       in request.META.items() if header.startswith('HTTP_'))
    res = {}
    res['type'] = 'init'
    res['status'] = 'ok'
    res['your_header'] = headers
    return JsonResponse(res)


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