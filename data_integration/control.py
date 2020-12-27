from .datamigrate import MyMigrationTest
from .models import *
from .myschedule import *
from .funcset import *
import datetime
import json
"""
根据id来形成具体的控制流信息，并交付给MySchedule来执行,**现在先以两个固定的表为例**
需要那些控制流信息？ 从哪里获取这些控制流信息
fun:数据迁移主体函数 --> datamigrate.py
host,prot,user,passwd,table_name,连接数据的信息，两份 --> FlowModel
date:调度所需的时间 --> ClusterModel
密码等信息后期重构时可以拆分出去，单独以一个表存储，只需要报错其id，然后到时候索引即可
"""


class MyControl():
    cluster = None
    flow = None
    func_tables = {'': max}
    node_type_table = {'source': ['timer', 'task'],
                       'func': ['clear'], 'target': ['end', 'over']}
    delete_type_table = ['id', 'name', 'type', 'top', 'ico', 'status']
    trigger_table = {0: '', 1: 'date', 2: 'interval', 3: 'cron'}
    func_params = []
    date_params = []

    def __init__(self) -> None:
        # super().__init__()
        # self.id = id
        self.my_schedule = MySchedule()
    """
    根据id来设置数据源
    """

    def _set_datasource(self, id):
        self.cluster = ClusterModel.objects.get(id=id)
        self.flow = FlowModel.objects.get(clusterOfFlow_id=id)

    def need_schedule(self, id):
        self._set_datasource(id)
        return self.cluster.update or self.flow.update

    def _get_info(self, id):
        self.func_params = []
        self._set_datasource(id)
        trigger_index = self.cluster.autoSuspend
        date_str = self.cluster.date
        flow_str = self.flow.dataOfFlow
        # date = datetime.strftime(date_str, "%M %H %d %m %Y")
        print(trigger_index)
        print(date_str)
        self.parseFlow(flow_str)
        return trigger_index, date_str

    def add(self, id):
        index, date = self._get_info(id)
        print("add schedule")
        print('func param:', self.func_params)
        print(index, date)
        if self.trigger_table[index] == 'date':
            pass
            # date = datetime.datetime.strptime(date, "%M %H %d %m %Y")
            # self.my_schedule.add_job()
        elif self.trigger_table[index] == 'interval':
            pass
        elif self.trigger_table[index] == 'cron':
            pass
        else:
            print('not set valid time span')

    def start(self, id):
        pass

    def pause(self, id):
        pass

    def delete(self, id):
        pass

    def parseDate(self, index, date):
        # 分 时 日 月 周/年

        if self.trigger_table[index] == 'date':
            pass
        elif self.trigger_table[index] == 'interval':
            pass
        elif self.trigger_table[index] == 'cron':
            pass
        else:
            print('not set valid time span')

    def parseFlow(self, flowdata):
        self.params = []
        temp = json.loads(flowdata)
        for func_node in temp['nodeList']:
            if func_node['type'] in self.node_type_table['func']:
                self.func_params = {}
                source_id = []
                target_id = []
                source_nodes = []
                target_nodes = []
                for line in temp['lineList']:
                    id_of_from = line['from']
                    id_of_to = line['to']
                    if func_node['id'] == id_of_from:
                        target_id.append(id_of_to)
                    elif func_node['id'] == id_of_to:
                        source_id.append(id_of_from)
                    else:
                        continue
                    # temp['lineList'].remove(line)
                for data_node in temp['nodeList']:
                    if data_node['id'] in source_id:
                        # for e in self.delete_type_table:
                        # data_node.pop(e)
                        source_nodes.append(data_node)
                    elif data_node['id'] in target_id:
                        # for e in self.delete_type_table:
                        # data_node.pop(e)
                        target_nodes.append(data_node)
                    else:
                        continue
                self.func_params['func'] = func_node['type']
                self.func_params['source'] = source_nodes
                self.func_params['target'] = target_nodes
                self.params.append(self.func_params)


if __name__ == "__main__":
    id = 2
    myc = MyControl()
    myc.add(id)
