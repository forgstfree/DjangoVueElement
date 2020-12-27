import os
from externalscript import execjar
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core import serializers
import json

from .myclass import MyClass
from .forms import LogForm
# import ExecJar to run myself jar
import sys
sys.path.append('..')

myclass = MyClass()
# Create your views here.


@csrf_exempt
def model_form_upload(request):
    response = {}
    print(request)
    if request.method == 'POST':
        form = LogForm(request.POST, request.FILES)
        print("********")
        print(form)
        print("********")
        print(request.FILES)
        print("********")
        print(request.POST)
        print("********")
        if form.is_valid():
            form.save()
            response['error_num'] = 0
    else:
        response['error_num'] = 1
    return JsonResponse(response)


def show_data(request):
    # num = request.Get['num']
    # 如果num比数据库中的记录数多则会。。。
    print("request")
    print(request)
    print(request.GET)
    need_all = bool(request.GET['all'])
    index = int(request.GET['index'])
    limit = int(request.GET['limit'])
    date = myclass.get_datas(need_all, index, limit)
    print(settings.MEDIA_ROOT)
    return JsonResponse(date)


def analysis_log(request):
    date = {}
    date['code'] = 22222
    jsonfiles = []
    logfilename = request.GET['filename']
    num = request.GET['linenum']
    print("*************")
    print(logfilename)
    print(num)
    print("*************")
    if num is '':
        num = ['100']
    else:
        num = num.split(' ')
    exec_jar = execjar.ExecJar()
    for i in range(len(num)):
        jsonfile = ''
        jsonfile = 'result/'+num[i]+logfilename.split('/')[1]+'.json'
        print("logfilename:", logfilename, " jsonfile:", jsonfile)
        jsonfiles.append(jsonfile)
        p = exec_jar.run(settings.MEDIA_ROOT+"/"+logfilename,
                         num[i], settings.MEDIA_ROOT+"/"+jsonfile)
    date['code'] = 20000
    date['jsonfiles'] = jsonfiles
    return JsonResponse(date)
