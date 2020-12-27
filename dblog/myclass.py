from .models import LogFileModel
from django.core import serializers
import json


class MyClass():
    def get_datas(self, need_all, index=1, limit=10):
        response = {}
        response['code'] = 20000
        try:
            response['total'] = LogFileModel.objects.count()
            if need_all:
                temp_all_datas = LogFileModel.objects.all()
            else:
                temp_all_datas = LogFileModel.objects.all()[
                    (index-1)*limit:(index*limit)]
            response['items'] = json.loads(
                serializers.serialize("json", temp_all_datas))
            response['msg'] = 'The record is return.'
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = 22222
        return response
