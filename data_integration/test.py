import json

node_type_table = {'source': ['timer', 'task'],
                   'func': ['clear'], 'target': ['end', 'over']}
delete_type_table = ['id', 'name', 'type', 'top', 'ico', 'status']
params = []


def parseFlow(flowdata):
    params = []
    temp = json.loads(flowdata)
    for func_node in temp['nodeList']:
        if func_node['type'] in node_type_table['func']:
            param = {}
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
            param['func'] = func_node['type']
            param['source'] = source_nodes
            param['target'] = target_nodes
            # print(param)
            params.append(param)
    print(params)


if __name__ == "__main__":
    flowstr = '{"name":"test1","nodeList":[{"id":"3fct25pftd","name":"数据接入","type":"timer","left":"86px","top":"57.599998474121094px","ico":"el-icon-time","state":"success"},{"id":"7g2bvb7q23","name":"接口调用","type":"task","left":"352px","top":"67.5999984741211px","ico":"el-icon-odometer","state":"success"},{"id":"y3ucox2nl","name":"数据清洗","type":"clear","left":"217px","top":"233.5999984741211px","ico":"el-icon-time","state":"success"},{"id":"pfyzk5iea","name":"流程结束","type":"end","left":"215px","top":"419px","ico":"el-icon-caret-right","state":"success"}],"lineList":[{"from":"3fct25pftd","to":"y3ucox2nl"},{"from":"7g2bvb7q23","to":"y3ucox2nl"},{"from":"y3ucox2nl","to":"pfyzk5iea"}]}'
    parseFlow(flowstr)

