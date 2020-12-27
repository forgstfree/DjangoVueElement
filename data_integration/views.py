from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .forms import *
from .models import *
import json

from .control import MyControl
# Create your views here.


myc = MyControl()


def getList(request):
    data = {}
    data['code'] = 22222
    if request.method == 'GET':
        m = {'1': ProjectModel, '2': ClusterModel,
             '3': FlowModel}
        mType = request.GET['model']
        mField = request.GET['field']
        index = int(request.GET['index'])
        limit = int(request.GET['limit'])
        if mField == '':
            data['total'] = m[mType].objects.count()
            temp_all_datas = m[mType].objects.all(
            )[(index-1)*limit:(index*limit)]
        else:
            mField = json.loads(mField)
            print(mField)
            print(type(mField))
            temp = m[mType].objects.filter(**mField)
            data['total'] = temp.count()
            temp_all_datas = temp[(index-1)*limit:(index*limit)]
            # data['total'] = m[mType].objects.filter(**mField).count()
            # temp_all_datas = m[mType].objects.filter(**mField)[(index-1)*limit:(index*limit-1)]
        all_datas = json.loads(serializers.serialize("json", temp_all_datas))
        data['items'] = all_datas
        data['code'] = 20000
        data['message'] = 'The record is return.'
    else:
        data['message'] = 'The request is not valid!'
    return JsonResponse(data)


@csrf_exempt
def getBrief(request):
    data = {}
    data['code'] = 22222
    if request.method == 'GET':
        m = {'1': ProjectModel, '2': ClusterModel}
        mType = request.GET['model']
        mValues = request.GET.getlist('values[]')
        temp_all_datas = m[mType].objects.all().values(*mValues)
        all_datas = json.dumps(list(temp_all_datas))
        data['items'] = all_datas
        data['code'] = 20000
        data['message'] = 'The data is return.'
    else:
        data['message'] = 'The request is not valid!'

    return JsonResponse(data)


def getProjectCluster(request):
    data = {}
    data['code'] = 22222
    if request.method == 'GET':
        projects = ProjectModel.objects.all().values('id', 'name')
        tempProject = []
        for p in projects:
            tempCluster = []
            clusters = ClusterModel.objects.filter(
                projectOfCluster=p['id']).values('id', 'name')
            for c in clusters:
                tempCluster.append(c)
            p['children'] = tempCluster
            tempProject.append(p)
        data['items'] = tempProject
        data['code'] = 20000
        data['message'] = 'The data is return.'
    else:
        data['message'] = 'The request is not valid!'

    return JsonResponse(data)


@csrf_exempt
def createData(request):
    data = {}
    data['code'] = 22222
    if request.method == 'POST':
        form = ''
        m = {1: ProjectForm, 2: ClusterForm, 3: FlowForm}
        x = json.loads(request.body)
        mType = x['model']
        fields = x['fields']
        print('*******')
        print(fields)
        print(type(fields))
        print('*******')
        form = m[mType](fields)
        print(form)
        print('*******')
        if form.is_valid():
            form.save()
            data['code'] = 20000
            data['message'] = 'The data is create.'
        else:
            data['message'] = 'The form data is not valid!'
    else:
        data['message'] = 'The request method is not POST!'
    return JsonResponse(data)


@csrf_exempt
def updateData(request):
    data = {}
    data['code'] = 22222
    if request.method == 'POST':
        m = {1: ProjectModel, 2: ClusterModel, 3: FlowModel}
        x = json.loads(request.body)
        print(x)
        mType = x['model']
        record = m[mType].objects.get(pk=x['pk'])
        record.__dict__.update(x['fields'])
        print(record)
        record.save()
        data['code'] = 20000
        data['message'] = 'The record is update.'

    return JsonResponse(data)


@csrf_exempt
def deleteData(request):
    data = {}
    data['code'] = 22222
    if request.method == 'GET':
        m = {'1': ProjectModel, '2': ClusterModel, '3': FlowModel}
        mType = request.GET['model']
        mField = request.GET['field']
        mField = json.loads(mField)
        print(mField)
        print(type(mField))
        temp = m[mType].objects.get(**mField).delete()
        data['code'] = 20000
        data['message'] = 'The record is delete.'
    else:
        data['message'] = 'The request is not valid!'

    return JsonResponse(data)


@csrf_exempt
def startScheduler(request):
    data = {}
    data['code'] = 22222
    if request.method == 'GET':
        id = request.GET['id']
        print("startScheduler is:", id)
        myc.add(id)
        data['code'] = 20000
        data['message'] = 'The record is delete.'
    else:
        data['message'] = 'The request is not valid!'

    return JsonResponse(data)


@csrf_exempt
def createFlowData(request):
    data = {}
    data['code'] = 22222
    if request.method == 'POST':

        data['code'] = 20000
        data['message'] = 'The data is update.'

    return JsonResponse(data)
